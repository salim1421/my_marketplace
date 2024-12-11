from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DeleteView, DetailView


from .forms import ReviewForm
from .models import (
    Store, SubCategory,
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


def cartView(request):
    cart_item = CartItem.objects.filter(
        user=request.user
    )
    total_price = sum(
        item.product.price * item.quantity for item in cart_item
        )
    context = {
        cart_item: 'cart_item', total_price:'total_price'
    }
    return render(request, 'base/cart_item.html', context)


def add_to_cart(request, product_id):
    pass


def remove_from_cart(request, product_id):
    pass

