from rest_framework import serializers
from base.models import (
    Order, CartItem,
    Products, Category, Store, 
    SubCategory, CheckOut,
    Payment
    )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'user',
            'products',
            'quantity',
        ]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    
class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckOut
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    category = SubcategorySerializer(read_only=True, source='subcategory_set', many=True)
    class Meta:
        model = Category
        fields =  '__all__'

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    pass