"""
Product Catalogue

Auto generated pages for Aunex products.

"""

from django.urls import path, re_path
from . import views

urlpatterns = [

    #new data entries
    re_path(r"new_image/?$", views.newImage, name="newImage"),
    re_path(r"new_product_type/?$", views.newProductType, name="newProductType"),
    re_path(r"new_product_category/?$", views.newProductCategory, name="newProductCategory"),
    re_path(r"new_product_series/?$", views.newProductSeries, name="newProductSeries"),
    re_path(r"new_product/?$", views.newProduct, name="newProduct"),
    re_path(r"new_product_manual/?$", views.newProductManual, name="newProductManual"),
    path("new_entry_submit/<str:type>", views.newEntrySubmit, name="newEntrySubmit"),

    #product pages
    path("<str:product>", views.product, name="product"),
    path("series/<str:series>", views.series, name="series"),

]
