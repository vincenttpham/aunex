"""
Main Navigation URLs

Home page and primary pages
Also hosts the user account services

Notes:
05/04/2021
Ported HTML pages from the previous site have only been edited for Django compability,
not formatting.

"""

from django.urls import path, re_path
from . import views

urlpatterns = [

    #home pages
    path("", views.index, name="index"),
    re_path(r"mobile/?$", views.mobile, name="mobile"),
    re_path(r"motorcycle/?$", views.motorcycle, name="motorcycle"),
    re_path(r"powersport/?$", views.powersport, name="powersport"),
    re_path(r"marine/?$", views.marine, name="marine"),
    re_path(r"dealerlocator/?$", views.dealerlocator, name="dealerlocator"),
    re_path(r"about/?$", views.about, name="about"),
    re_path(r"support/?$", views.support, name="support"),
    re_path(r"contact/?$", views.contact, name="contact"),

    #user login
    re_path(r"login/?$", views.loginPage, name="login"),
    re_path(r"logout/?$", views.logoutPage, name="logout"),
    re_path(r"changepassword/?$", views.changePassword, name="changePassword"),
    re_path(r"createuser/?$", views.createUser, name="createUser"),

    #dealer locator
    re_path(r"dealer-locations/?$", views.dealerLocations, name="dealerLocations"),
    re_path(r"aunex-dealer-locator/?$", views.aunexdealerlocator, name="aunexdealerlocator")

]
