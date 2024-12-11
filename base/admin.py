from django.contrib import admin
from .models import (
    CartItem, Category,
    Products, Review,
    Order, Store,
    SubCategory
)

class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'price',
        'date_created',
    ]
    search_fields = ['name']
    fieldsets = [
        (None, {'fields':['name']}),
        ('Product Details', {'fields':[
            'image',
            'price',
            'category',
            'subcategory',
            'store',
            'date_created'
            ]})
    ]
    list_filter = ['date_created']


class StoreAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'address'
    ]
    search_fields = ['name']


class SubCategoryAdmin(admin.TabularInline):
    model = SubCategory
    extra = 3


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]
    search_fields = ['name']
    inlines = [SubCategoryAdmin]


admin.site.register(Products, ProductAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review)
