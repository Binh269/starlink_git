from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('msp', 'tensp', 'gia')
    search_fields = ('msp', 'tensp')
    list_filter = ('gia',)
