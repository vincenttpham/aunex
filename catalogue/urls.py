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
    re_path(r"new_dealer/?$", views.newDealer, name="newDealer"),
    path("new_entry_submit/<str:type>/", views.newEntrySubmit, name="newEntrySubmit"),
    path("upload_dealers/", views.uploadDealers, name="uploadDealers"),
    path("update_dealers/", views.updateDealers, name="updateDealers"),
    path("inventory/", views.inventory, name="inventory"),
    path("inventory/update/", views.updateInventory, name="updateInventory"),
    path("documents/", views.documents, name="documents"),
    path("catalogue/", views.catalogue, name="catalogue"),
    path("rep_order/", views.rep_order, name="rep_order"),
    path("cart/", views.cartView, name="cart"),
    path("cart/info/", views.billing_info, name="billing_info"),
    path("cart/add/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<str:name>", views.remove_from_cart, name="remove_from_cart"),
    path("cart/change_quantity/", views.change_quantity, name="change_quantity"),
    path("order/place/", views.place_order, name="place_order"),
    path("order/<int:id>/", views.order_summary, name="orderSummary"),
    path("order/all/", views.all_orders, name="all_orders"),
    path("media/", views.mediaAssets, name="mediaAssets"),
    path("searchProducts/", views.searchProducts, name="searchProducts"),

    #product pages
    path("<str:product>", views.product, name="product"),
    path("series/<str:series>", views.series, name="series"),

]
