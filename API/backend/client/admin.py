from django.contrib import admin
from .models import Product, Sales, Supplier

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('product_id','name','price','supplier','product_type','expiry_duration', 'type_of_storage')

@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display=('product', 'date','search_interest','units_sold')
    search_fields=['product','date']

from .models import ProductInventory

@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'current_amount', 'safe_stock','shelf_life', 'reorder_point',
                     'lead_time','lead_time_unit', 'fulfillment_time','fulfillment_time_unit', 'needs_restock')


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display=('supplier_id','name','address','lead_time', 'min_order_amount')

