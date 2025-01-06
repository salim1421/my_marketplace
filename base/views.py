import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DeleteView, DetailView
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY
from .forms import CheckoutForm, ReviewForm
from .models import (
    CheckOut, Payment, Store, SubCategory,
    CartItem, Category,
    Products, Order,
    Review,
)


class ProductListView(ListView):
    model = Products
    paginate_by = 5
    ordering = ['-id']
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Products

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        review = Review.objects.filter(product=self.get_object())
        if self.request.user.is_authenticated:
            context['review_form'] = ReviewForm(instance=self.request.user)

        context["reviews"] = review
        return context
    
    def post(self, request, *args, **kwargs):
        new_review = Review(
            product=self.get_object(),
            name=request.user,
            body=request.POST['body']
        )
        new_review.save()
        return self.get(self, request, *args, **kwargs)
    

def sub_categoryList(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    context = {'categories':category}
    return render(request, 'base/categories.html', context)

class StoreListView(ListView):
    model = Store
    context_object_name = 'stores'
    ordering = '-name'


class SubCategoryView(DetailView):
    model = SubCategory
    template_name = 'base/subcategory.html'

    def get_context_data(self, **kwargs):
        context = super(SubCategoryView, self).get_context_data(**kwargs)
        subcat = get_object_or_404(SubCategory, id=self.kwargs['pk'])
        products = Products.objects.filter(subcategory=subcat)
        context["products"] = products
        return context
    
    

class StoreView(DetailView):
    model = Store
    template_name = 'base/store.html'

    def get_context_data(self, **kwargs):
        context = super(StoreView, self).get_context_data(**kwargs)
        store = get_object_or_404(Store, id=self.kwargs['pk'])
        products = Products.objects.filter(store=store)

        context["stores"] = products
        return context
    
    
    
def category_list(request):
    category = Category.objects.all()
    context = {
        'category_list': category 
    }
    return render(request, 'base/category.html', context)


def add_to_cart(request, pk):
    product = get_object_or_404(Products, id=pk)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        products=product,
        ordered=False 
    )
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        if order.cart_item.filter(products__pk=product.pk):
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, 'Item Quantity Updated')
        else:
            order.cart_item.add(cart_item)
            order.save()
            messages.info(request, 'Product Added To Your Cart')
            return redirect('product-detail', pk=pk)
        
    else:
        time = timezone.now()
        order = Order.objects.create(user=request.user, ordered_on=time)
        order.cart_item.add(cart_item)
        order.save()
        messages.success(request, 'Item Order Has been Added Successfully')

    return HttpResponseRedirect(reverse('product-detail', args=[str(pk)]))


def reduce_from_cart(request, pk):
    product = get_object_or_404(Products, pk=pk)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        products=product,
        ordered=False
    )
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        if order.cart_item.filter(products__pk=product.pk).exists():
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            messages.info(request, 'Item Quantity Updated')
            return redirect('cart')
        else:
            messages.info(request, 'Item Quantity Removed')
            return redirect('cart')
        
    else:
        messages.info(request, 'You Do Not Have An Order')
    return redirect('cart')


def add_cart(request, pk):
    product = get_object_or_404(Products, pk=pk)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        products=product,
        ordered=False
    )
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.cart_item.filter(products__pk=product.pk).exists():
            cart_item.quantity += 1
            cart_item.save()
            messages.info(request, 'Item Quantity Added')
        return redirect('cart')


def cartItemList(request):
    cart_item = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    context = {
        'order':cart_item,
    }
    
    return render(request, 'base/cart_item.html', context)


def remove_from_cart(request, pk):
    product = get_object_or_404(Products, pk=pk)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        products=product,
        ordered=False
    )
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.cart_item.filter(products__pk=product.pk).exists():
            cart_item = CartItem.objects.filter(
                user=request.user,
                ordered=False,
                products=product
            )
            cart_item.delete()
            messages.info(request, 'Item Deleted From Your Cart')
            return redirect('cart')
        else:
            messages.info(request, 'Item Does Not Exist In Your Cart')
            return redirect('cart')
    else:
        messages.info(request, 'You Do Not Have An Order')
    return redirect('cart')


class CheckoutView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = CheckoutForm()
        context = {
            'order':order,
            'form':form
        }
        return render(self.request, 'base/checkout.html', context)
    
    def post(self, *args, **kwargs):
        
        form = CheckoutForm(self.request.POST or None)

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                address = form.cleaned_data.get('address')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')
                payment = form.cleaned_data.get('payment')

                checkout_address = CheckOut(
                    user=self.request.user,
                    address=address,
                    country=country,
                    zip_code=zip_code
                )
                checkout_address.save()
                order.checkout_address = checkout_address
                order.save()

                if payment == 'S':
                    return redirect('payment', payment='stripe')
                elif payment == 'P':
                    return redirect('payment', payment='paypal')
                else:
                    messages.error(self.request, 'Invalid Payment Option')
                    return redirect('cart')
        except Order.DoesNotExist:
            messages.error(self.request, "You Don't Have An Order")
        return redirect('cart')


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
         
        context = {
            'order':order,
            "stripe_public_key":settings.STRIPE_PUBLIC_KEY
        }
        return render(self.request, 'base/payment.html', context)

    def post(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            token = self.request.POST.get('stripeToken')
            amount = int(order.get_final_price() * 100)
            cart_item = CartItem.objects.filter(user=self.request.user, ordered=False)

            charge = stripe.Charge.create(
                currency='usd',
                amount=amount,
                source=token
            )

            payment = Payment()
            payment.user = self.request.user
            payment.amount = order.get_final_price()
            payment.stripe_id = charge['id']
            payment.save()

            cart_item.ordered = True
            order.ordered = True
            order.payment = payment
            order.save()
            
            messages.success(self.request, 'You Have Successfully Place Your Order')
            return redirect('/')
        except stripe.CardError:
            messages.error(self.request, 'Error Process Your Card')
            return redirect('checkout')
        

@csrf_exempt
def process_payment(request):
    order = Order.objects.get(user=request.user, ordered=False)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            payment_method_id = data.get('payment_method_id')

            intent = stripe.PaymentIntent.create(
                payment_method=payment_method_id,
                currency='usd',
                amount=int(order.get_final_price() * 100),
                return_url='http://127.0.0.1:8000/',
                confirm=True,
                confirmation_method='manual'
            )
            return JsonResponse({'success': True})
        except stripe.error.CardError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid Request'}, status=400)
        
