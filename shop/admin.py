from django.contrib import admin
from .models import Category, Product, SaleRecord
from parler.admin import TranslatableAdmin


# Register your models here.

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}



@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'stock', 'price_customer', 'price_vendor','available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['stock', 'price_customer', 'price_vendor', 'available']
    
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}
    

@admin.register(SaleRecord)
class SaleRecordAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity']