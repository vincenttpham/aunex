from django.contrib.auth import authenticate, login, logout
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.templatetags.static import static

import csv
from django.contrib.staticfiles import finders

from .models import User
from catalogue.models import ProductSeries, ProductType, Category

#home page
def index(request):

    #get featured products

    #amps
    typeAmp = None
    amps = None
    if(ProductType.objects.filter(name="Amplifier").exists()):
        typeAmp = ProductType.objects.get(name="Amplifier")
    if(typeAmp):
        amps = ProductSeries.objects.filter(type=typeAmp)

    #eq
    typeEq = None
    eqs = None
    if(ProductType.objects.filter(name="Equalizer").exists()):
        typeEq = ProductType.objects.get(name="Equalizer")
    if(typeEq):
        eqs = ProductSeries.objects.filter(type=typeEq)
    
    #acc
    typeAcc = None
    accs = None
    if(ProductType.objects.filter(name="Accessory").exists()):
        typeAcc = ProductType.objects.get(name="Accessory")
    if(typeAcc):
        accs = ProductSeries.objects.filter(type=typeAcc)

    #render page
    return render(request, "main/index.html", {
        "amps": amps,
        "eqs": eqs,
        "accs": accs
    })

#mobile page
def mobile(request):

    #get mobile products
    p = getProductSeries("Mobile")

    return render(request, "main/mobile.html", {
        "amps": p[0],
        "eqs": p[1],
        "accs": p[2]
    })

#motorcycle page
def motorcycle(request):

    #get motorcycle products
    p = getProductSeries("Motorcycle")

    return render(request, "main/motorcycle.html", {
        "amps": p[0],
        "eqs": p[1],
        "accs": p[2]
    })

#powersport page
def powersport(request):

    #get powersport products
    p = getProductSeries("Powersport")

    return render(request, "main/powersport.html", {
        "amps": p[0],
        "eqs": p[1],
        "accs": p[2]
    })

#marine page
def marine(request):
    
    #get marine products
    p = getProductSeries("Marine")

    return render(request, "main/marine.html", {
        "amps": p[0],
        "eqs": p[1],
        "accs": p[2]
    })

#dealer locator page
def dealerlocator(request):
    return render(request, "main/dealerlocator.html")

#about page
def about(request):
    return render(request, "main/about.html")

#support page
def support(request):
    return render(request, "main/support.html")

#contact page
def contact(request):
    return render(request, "main/contact.html")

#register a new user
@login_required
def createUser(request):
    #only staff should be able to access this page
    if request.user.is_staff:

        if request.method == "POST":
            username = request.POST["username"]
            email = request.POST["email"]

            #ensure password matches confirmation
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
            if password != confirmation:
                return render(request, "main/createuser.html", {
                    "message": "The passwords must match."
                })

            #attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                return render(request, "main/createuser.html", {
                    "message": "Username already taken."
                })
            return render(request, "main/createuser.html", {
                    "message": "User created successfully. Check the Admin Panel to verify."
                })

        else:
            return render(request, "main/createuser.html")

    return HttpResponseRedirect(reverse("index"))

#login page
# POST - log the user in
def loginPage(request):
    if request.method == "POST":

        #attempt to sign the user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        #check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "main/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "main/login.html")

#change password
@login_required
def changePassword(request):
    if request.method == "POST":
        oldPassword = request.POST["password"]
        if request.user.check_password(oldPassword): #password correct

            newPassword = request.POST["newPassword"]
            confirmation = request.POST["confirmation"]

            if newPassword == confirmation: #set new password
                request.user.set_password(newPassword)
                request.user.save()
                return render(request, "main/changepassword.html", {
                    "message": "Password changed successfully."
                })

            else:
                return render(request, "main/changepassword.html", {
                    "message": "Confirmation did not match your new password. Please try again."
                })
        
        else: #password incorrect
            return render(request, "main/changepassword.html", {
                "message": "Password incorrect. Please try again."
            })
    
    else:
        return render(request, "main/changepassword.html")

#logout
def logoutPage(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

#aunex dealer locator iframe
@xframe_options_exempt
def aunexdealerlocator(request):
    return render(request, "main/aunexdealerlocator.html")

#return dealer locations
def dealerLocations(request):
    #return locations and addresses
    if request.method == "GET":
        return JsonResponse(locationstoArray())

    #must be via GET 
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)

#returns 2D array of first and second column
def locationstoArray() -> dict:
    results = {}
    f = open(finders.find('main/locations.csv'))
    reader = csv.reader(f)
    a = []
    b = []
    for row in reader:
        a.append(row[0])
        b.append(row[1])
    results["locations"] = a
    results["addresses"] = b
    f.close()
    return results

#returns product series for a specific category
def getProductSeries(category):
    
    if(Category.objects.filter(name=category).exists()):

        cat = Category.objects.get(name=category)

        #amps
        typeAmp = None
        amps = None
        if(ProductType.objects.filter(name="Amplifier").exists()):
            typeAmp = ProductType.objects.get(name="Amplifier")
        if(typeAmp):
            amps = ProductSeries.objects.filter(type=typeAmp, category=cat)

        #eq
        typeEq = None
        eqs = None
        if(ProductType.objects.filter(name="Equalizer").exists()):
            typeEq = ProductType.objects.get(name="Equalizer")
        if(typeEq):
            eqs = ProductSeries.objects.filter(type=typeEq, category=cat)
        
        #acc
        typeAcc = None
        accs = None
        if(ProductType.objects.filter(name="Accessory").exists()):
            typeAcc = ProductType.objects.get(name="Accessory")
        if(typeAcc):
            accs = ProductSeries.objects.filter(type=typeAcc, category=cat)

        return [amps, eqs, accs]
    
    else:

        return [None, None, None]
