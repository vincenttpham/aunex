from django.contrib import admin
from .models import ProductSeries, Product, Image, ProductType, Category, Manual, Dealer, Document, LastUpdate, Video, CartProduct, Cart, Order

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductSeries)
admin.site.register(Category)
admin.site.register(ProductType)
admin.site.register(Image)
admin.site.register(Manual)
admin.site.register(Dealer)
admin.site.register(Document)
admin.site.register(LastUpdate)
admin.site.register(Video)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Order)