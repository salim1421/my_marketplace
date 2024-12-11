from django.urls import path
from .views import (
    ProductDetailView, ProductListView,
    StoreListView, StoreView,
    SubCategoryView, sub_categoryList,
    category_list, cartView,
    add_to_cart, remove_from_cart
)


urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('product/detail/<str:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('store/list', StoreListView.as_view(), name='store-list'),
    path('store/<str:pk>', StoreView.as_view(), name='store'),
    path('category/<category_id>', sub_categoryList, name='category'),
    path('subcategory/<str:pk>', SubCategoryView.as_view(), name='subcategory'),
    path('categories', category_list, name='categories'),
    path('cart/items', cartView, name='cart'),
    path('add/to/cart/<product_id>', add_to_cart, name='add-to-cart'),
    path('remove/from/cart/<product_id>', remove_from_cart, name='remove-from-cart')
]
