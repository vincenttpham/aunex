from django.contrib import admin

from .models import ProductSeries, Product, Image, ProductType, Category, Manual

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductSeries)
admin.site.register(Category)
admin.site.register(ProductType)
admin.site.register(Image)
admin.site.register(Manual)
