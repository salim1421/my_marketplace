from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView, 
    RetrieveAPIView, DestroyAPIView,
    ListAPIView
    )

from .serializer import (
    PaymentSerializer, ProductSerializer,
    CartItemSerializer, CategorySerializer,
    SubcategorySerializer, OrderSerializer,
    CheckoutSerializer, StoreSerializer,
    UserSerializer,
)
from base.models import (
    Payment, Products,
    CartItem, Category,
    Store, SubCategory,
    Order, CheckOut
)


class ProducListView(ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer


class ProductCreateView(CreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


class ProductUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'


class CategoryUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'


class SubcategoryListView(ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubcategorySerializer


class SubcategoryCreateView(CreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubcategorySerializer


class SubcategoryDetailView(RetrieveAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubcategorySerializer
    lookup_field = 'pk'


class SubcategoryUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubcategorySerializer
    lookup_field = 'pk'


class CartItemListView(ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CartItemCreateView(CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CartItemDetailView(RetrieveAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    lookup_field = 'pk'


class CartItemUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    lookup_field = 'pk'


class OrderListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'


class OrderUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = CartItemSerializer
    lookup_field = 'pk'


class PaymentListView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentCreateView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDetailView(RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = 'pk'


class PaymentDeleteView(DestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = 'pk'


class CheckoutListView(ListAPIView):
    queryset = CheckOut.objects.all()
    serializer_class = CheckoutSerializer


class CheckoutDetailView(RetrieveAPIView):
    queryset = CheckOut.objects.all()
    serializer_class = CheckoutSerializer
    lookup_field = 'pk'


class CheckoutUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = CheckOut.objects.all()
    serializer_class = CheckoutSerializer
    lookup_field = 'pk'


class StoreListView(ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class StoreCreateView(CreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    lookup_field = 'pk'


class StoreDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    lookup_field = 'pk'
