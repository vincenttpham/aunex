from django.contrib.auth.models import Group
from django.utils import html
from os import name
from django.db.models.aggregates import Sum
from django.shortcuts import redirect, render
from django.forms import ModelForm
from catalogue.models import Cart, CartProduct, Document, Image, LastUpdate, Order, Product, ProductSeries, ProductType, Category, Manual, Dealer, LastUpdate, Video
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.db.models import Q
from django.db.models import Count

from django.core.mail import EmailMultiAlternatives, message
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.conf import settings

from .models import User

import requests
import decimal

# FORMS ----------------------------------------------------------

#form for creating a new product type
class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['image']

#form for creating a new product type
class ProductTypeForm(ModelForm):
    class Meta:
        model = ProductType
        fields = ['name']

#form for creating a new product categorey
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']

#form for creating a new product series
class ProductSeriesForm(ModelForm):
    class Meta:
        model = ProductSeries
        fields = ['name', 'image', 'banner', 'products', 'summary', 'description', 'category', 'type', 'infoImage']

#form for creating a new product
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'gallery', 'summary', 'specSheet', 'file']

#form for creating a new product
class ProductManualForm(ModelForm):
    class Meta:
        model = Manual
        fields = ['file']

#form for updating dealer locations
class DealerForm(ModelForm):
    class Meta:
        model = Dealer
        fields = ['name', 'telephone', 'address', 'city', 'state', 'zipcode', 'website', 'brand', 'elite', 'latitude', 'longitude']

#form for uploading documents
class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ['file']

# VIEWS ----------------------------------------------------------

# FORMS ----------------------------------------------------------

#new image form
@login_required
def newImage(request):
    return render(request, "catalogue/newEntry.html", {
        "type": "newImage",
        "entryForm": ImageForm()
    })

#new product type form
@login_required
def newProductType(request):
    return render(request, "catalogue/newEntry.html", {
        "type": "newProductType",
        "entryForm": ProductTypeForm()
    })

#new product category form
@login_required
def newProductCategory(request):
    return render(request, "catalogue/newEntry.html", {
        "type": "newProductCategory",
        "entryForm": CategoryForm()
    })

#new product series form
@login_required
def newProductSeries(request):
    return render(request, "catalogue/newEntry.html", {
        "type": "newProductSeries",
        "entryForm": ProductSeriesForm()
    })

#new product form
@login_required
def newProduct(request):
    return render(request, "catalogue/newEntry.html", {
        "type": "newProduct",
        "entryForm": ProductForm()
    })

#new product manual form
@login_required
def newProductManual(request):
    return render(request, "catalogue/newEntry.html", {
        "type": "newProductManual",
        "entryForm": ProductManualForm()
    })

#new dealer
@login_required
def newDealer(request):
    dealers = Dealer.objects.all()
    update = ''
    if dealers.filter(latitude=None, longitude=None).count() > 0:
        update = 'required'
    last_update = ''
    if LastUpdate.objects.filter(name='Dealers').exists():
        last_update = LastUpdate.objects.get(name='Dealers')
    return render(request, "catalogue/newEntry.html", {
        "type": "newDealer",
        "entryForm": DealerForm(),
        "dealers": dealers,
        "update": update,
        "last_update": last_update
    })

#submit new data
@login_required
def newEntrySubmit(request, type):
    #only staff should be able to access this page
    if request.user.is_staff:
        if request.method == "POST":
            
            if type == "newImage":
                #create new entry
                f = ImageForm(request.POST, request.FILES)
                if f.is_valid():
                    n = f.save()
                else: #invalid form
                    return render(request, "catalogue/newEntry.html", {
                        "type": "newImage",
                        "entryForm": f
                    })
                #redirect back to the form
                return newImage(request)

            elif type == "newProductCategory":
                #create new entry
                f = CategoryForm(request.POST, request.FILES)
                if f.is_valid():
                    n = f.save()
                else: #invalid form
                    return render(request, "catalogue/newEntry.html", {
                        "type": "newProductCategory",
                        "entryForm": f
                    })
                #redirect back to the form
                return newProductCategory(request)
    
            elif type == "newProductType":
                #create new entry
                f = ProductTypeForm(request.POST, request.FILES)
                if f.is_valid():
                    n = f.save()
                else: #invalid form
                    return render(request, "catalogue/newEntry.html", {
                        "type": "newProductType",
                        "entryForm": f
                    })
                #redirect back to the form
                return newProductType(request)
            
            elif type == "newProductManual":
                #create new entry
                f = ProductManualForm(request.POST, request.FILES)
                if f.is_valid():
                    n = f.save()
                else: #invalid form
                    return render(request, "catalogue/newEntry.html", {
                        "type": "newProductManual",
                        "entryForm": f
                    })
                #redirect back to the form
                return newProductManual(request)
            
            elif type == "newProduct":
                #create new entry
                f = ProductForm(request.POST, request.FILES)
                if f.is_valid():
                    n = f.save()
                else: #invalid form
                    return render(request, "catalogue/newEntry.html", {
                        "type": "newProduct",
                        "entryForm": f
                    })
                #redirect back to the form
                return newProduct(request)
            
            elif type == "newProductSeries":
                #create new entry
                f = ProductSeriesForm(request.POST, request.FILES)
                if f.is_valid():
                    n = f.save()
                else: #invalid form
                    return render(request, "catalogue/newEntry.html", {
                        "type": "newProductSeries",
                        "entryForm": f
                    })
                #redirect back to the form
                return newProductSeries(request)
            
            elif type == "newDealer":
                #update dealer list
                f = DealerForm(request.POST, request.FILES)
                if f.is_valid():
                    n = f.save()
                else: #invalid form
                    return render(request, "catalogue/newEntry.html", {
                        "type": "newDealer",
                        "entryForm": f
                    })
                return newDealer(request)
            
    elif request.user.groups.filter(name='Dealer Manager').exists():
        if request.method == "POST":
            if type == "newDealer":
                #update dealer list
                f = DealerForm(request.POST, request.FILES)
                if f.is_valid():
                    n = f.save()
                else: #invalid form
                    return render(request, "catalogue/newEntry.html", {
                        "type": "newDealer",
                        "entryForm": f
                    })
                return newDealer(request)
    
    return HttpResponseRedirect(reverse("index"))

# GENERATED PAGES ----------------------------------------------------------

#page for a product
def product(request, product):

    #get requested product
    pr = Product.objects.get(name=product)


    return render(request, "catalogue/productPage.html", {
        "product": pr
    })

#page for a series
def series(request, series):

    #get the requested series
    se = ProductSeries.objects.get(name=series)

    return render(request, "catalogue/seriesPage.html", {
        "series": se
    })

# NEW ----------------------------------------------------------

#inventory
@login_required
def inventory(request):
    inventory_manager = ''
    stock = Product.objects.filter(pop=False)
    if request.user.is_staff or request.user.groups.filter(name='Inventory Manager').exists():
        inventory_manager = Group.objects.get(name='Inventory Manager')
        stock = Product.objects.all()
    last_update = ''
    if LastUpdate.objects.filter(name='Inventory').exists():
        last_update = LastUpdate.objects.get(name='Inventory')
    context = {
        "inventory_manager": inventory_manager,
        "stock": stock,
        "last_update": last_update
    }
    return render(request, "catalogue/inventory.html", context)

#documents
@login_required
def documents(request):
    products = Product.objects.all()
    docs = Document.objects.order_by('-uploaded_at')
    context = {
        "docs": docs,
        "products": products
    }
    return render(request, "catalogue/documents.html", context)

#rep orders
@login_required
def rep_order(request):
    if request.method == "POST":
        try:
            xlsx_file = request.FILES["xlsx_file"]
            if not xlsx_file.name.endswith('.xlsx'):
                messages.error(request,'File is not XLSX type')
                return redirect(rep_order)
            #if file is too large, return
            if xlsx_file.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (xlsx_file.size/(1000*1000),))
                return redirect(rep_order)
            
            #send order to email
            email = EmailMessage(
                'Rep Order',
                f'Order from {request.user.username}',
                f'Aunex <{settings.EMAIL_HOST_USER}>',
                [],
                settings.EMAIL_ORDER_RECIPIENTS,
                reply_to=[settings.EMAIL_HOST_USER],
                headers={'Message-ID': 'foo'},
            )
            email.attach(xlsx_file.name, xlsx_file.read(), xlsx_file.content_type)
            email.send(fail_silently=False)
            messages.info(request, "Order submitted successfully.")

        except Exception as e:
            messages.error(request,"Unable to upload file. "+repr(e))

        return redirect(rep_order)

    order_form = Document.objects.filter(Q(name__icontains='Order') | Q(file__icontains='Order')).order_by('-uploaded_at')
    if order_form:
        order_form = order_form[0]
    
    context = {
        "order_form": order_form
    }

    return render(request, "catalogue/repOrder.html", context)

#search all products
def searchProducts(request):
    products = Product.objects.all()
    series = ProductSeries.objects.all()
    search = ''
    type = ''
    channels = ''
    if 'search' in request.GET:
        search = request.GET['search']
        product_category = Category.objects.filter(name__icontains=search)
        product_type = ProductType.objects.filter(name__icontains=search)
        product_series = ProductSeries.objects.filter(Q(name__icontains=search) | Q(category__in=product_category) | Q(type__in=product_type))
        products = Product.objects.filter(Q(name__icontains=search) | Q(products__in=product_series))
    if 'type' in request.GET:
        if ProductType.objects.filter(name=request.GET['type']).exists():
            type = ProductType.objects.get(name=request.GET['type'])
            series = ProductSeries.objects.filter(type=type)
    if 'channels' in request.GET:
        channels = f".{request.GET['channels']}"
        type = ProductType.objects.get(name='Amplifier')
        series = ProductSeries.objects.filter(type=type)
    context = {
        "products": products,
        "series": series,
        "search": search,
        "type": type,
        "channels": channels
    }
    return render(request, "catalogue/searchProducts.html", context)

#catalogue for cart items
@login_required
def catalogue(request):
    products = Product.objects.all()
    series = ProductSeries.objects.all()
    search_catalogue = ''
    category = ''
    if 'search_catalogue' in request.GET:
        search_catalogue = request.GET['search_catalogue']
        products = Product.objects.filter(name__icontains=search_catalogue)
    if 'category' in request.GET:
        if ProductType.objects.filter(name=request.GET['category']).exists():
            category = ProductType.objects.get(name=request.GET['category'])
            series = ProductSeries.objects.filter(type=category)
    context = {
        "products": products,
        "series": series,
        "search_catalogue": search_catalogue,
        "category": category
    }
    return render(request, "catalogue/catalogue.html", context)

#review cart
@login_required
def cartView(request):
    series = ProductSeries.objects.all()
    cart = Cart.objects.filter(user=request.user)
    musway = series.filter(name='Musway DSP')
    if musway:
        musway = ProductSeries.objects.get(name='Musway DSP')

    cart_total = round(decimal.Decimal(0.00), 2)
    musway_total = round(decimal.Decimal(0.00), 2)
    cart_weight = 0
    musway_weight = 0

    for s in series:
        sum = 0
        msum = 0
        weight = 0
        mweight = 0
        if cart:
            cart = Cart.objects.get(user=request.user)
            for item in cart.products.all():
                if item.series == s:
                    sum += item.total
                    weight += item.weight
                if item.series == musway:
                    msum += item.total
                    mweight += item.weight
        s.total = round(decimal.Decimal(sum), 2)
        cart_total += sum
        musway_total += msum
        cart_weight += weight
        musway_weight += mweight

    aunex_total = cart_total - musway_total
    aunex_weight = cart_weight - musway_weight

    context = {
        "series": series,
        "cart": cart,
        "cart_total": cart_total,
        "aunex_total": aunex_total,
        "aunex_weight": aunex_weight,
        "musway_total": musway_total,
        "musway_weight": musway_weight
    }
    return render(request, "catalogue/cart.html", context)

#continue to order info
@login_required
def billing_info(request):
    series = ProductSeries.objects.all()
    cart = Cart.objects.filter(user=request.user)
    musway = series.filter(name='Musway DSP')
    if musway:
        musway = ProductSeries.objects.get(name='Musway DSP')

    cart_total = round(decimal.Decimal(0.00), 2)
    musway_total = round(decimal.Decimal(0.00), 2)
    cart_weight = 0
    musway_weight = 0

    for s in series:
        sum = 0
        msum = 0
        weight = 0
        mweight = 0
        if cart:
            cart = Cart.objects.get(user=request.user)
            for item in cart.products.all():
                if item.series == s:
                    sum += item.total
                    weight += item.weight
                if item.series == musway:
                    msum += item.total
                    mweight += item.weight
        s.total = round(decimal.Decimal(sum), 2)
        cart_total += sum
        musway_total += msum
        cart_weight += weight
        musway_weight += mweight
    
    last_order = Order.objects.filter(user=request.user).order_by('-created_at')
    if last_order:
        last_order = last_order[0]

    aunex_total = cart_total - musway_total
    aunex_weight = cart_weight - musway_weight

    context = {
        "series": series,
        "cart": cart,
        "cart_total": cart_total,
        "aunex_total": aunex_total,
        "aunex_weight": aunex_weight,
        "musway_total": musway_total,
        "musway_weight": musway_weight,
        "last_order": last_order
    }
    return render(request, "catalogue/billingInfo.html", context)

#all orders
@login_required
def order_summary(request, id):
    series = ProductSeries.objects.all()
    musway = series.filter(name='Musway DSP')
    if musway:
        musway = ProductSeries.objects.get(name='Musway DSP')
    order_total = round(decimal.Decimal(0.00), 2)
    musway_total = round(decimal.Decimal(0.00), 2)
    order_weight = 0
    musway_weight = 0
    order = Order.objects.get(id=id)
    for s in series:
        sum = 0
        msum = 0
        weight = 0
        mweight = 0
        for item in order.products.all():
            if item.series == s:
                sum += item.total
                weight += item.weight
            if item.series == musway:
                msum += item.total
                mweight += item.weight
        s.total = round(decimal.Decimal(sum), 2)
        order_total += sum
        musway_total += msum
        order_weight += weight
        musway_weight += mweight
    aunex_total = order_total - musway_total
    aunex_weight = order_weight - musway_weight
    context = {
        "series": series,
        "order": order,
        "order_total": order_total,
        "aunex_total": aunex_total,
        "aunex_weight": aunex_weight,
        "musway_total": musway_total,
        "musway_weight": musway_weight
    }
    return render(request, "catalogue/orderSummary.html", context)

#all orders
@login_required
def all_orders(request):
    if request.user.is_staff:
        orders = Order.objects.all().order_by('-created_at')
        context = {
            "orders": orders
        }
    elif request.user.groups.filter(name='Dealers').exists():
        orders = Order.objects.filter(user=request.user)
        context = {
            "orders": orders
        }
    return render(request, "catalogue/orders.html", context)

#add to cart
@login_required
def add_to_cart(request):
    if request.user.is_staff or request.user.groups.filter(name='Dealers').exists():
        if request.method == 'POST':
            if Cart.objects.filter(user=request.user).exists():
                cart = Cart.objects.get(user=request.user)
            else:
                cart = Cart.objects.create(user=request.user)
            product = Product.objects.get(name=request.POST.get('name'))
            series = ProductSeries.objects.all()
            for s in series:
                if product in s.products.all():
                    series = s
            if CartProduct.objects.filter(product=product, cart=cart).exists():
                cart_product = CartProduct.objects.get(product=product, cart=cart)
            else:
                cart_product = CartProduct.objects.create(product=product, series=series)
                cart.products.add(cart_product)
                cart.save()
            qty = int(request.POST['quantity'])
            if qty == 0:
                qty = 1
            cart_product.quantity += qty
            cart_product.total = decimal.Decimal(cart_product.total) + (product.price * decimal.Decimal(qty))
            cart_product.weight = decimal.Decimal(cart_product.weight) + (product.weight * decimal.Decimal(qty))
            cart_product.save()
            messages.info(request, f"{product.name} ({qty}) has been added to cart.")
    return redirect(catalogue)

#remove from cart
@login_required
def remove_from_cart(request, name):
    if request.user.is_staff or request.user.groups.filter(name='Dealers').exists():
        cart = Cart.objects.get(user=request.user)
        product = Product.objects.get(name=name)
        cart_products = CartProduct.objects.filter(product=product, cart=cart)
        for item in cart_products:
            item.delete()
        messages.info(request, f"{product.name} has been removed from cart.")
    return redirect(cartView)

#change item quantities
def change_quantity(request):
    if request.user.is_staff or request.user.groups.filter(name='Dealers').exists():
        if request.method == 'POST':
            cart = Cart.objects.get(user=request.user)
            product = Product.objects.get(name=request.POST.get('name'))
            cart_product = CartProduct.objects.get(product=product, cart=cart)
            if cart_product.quantity == int(request.POST.get('quantity')):
                messages.info(request, f"{product.name} x{cart_product.quantity} already in cart. Item quantity has not changed.")
                return redirect(cartView)
            else:
                cart_product.quantity = request.POST['quantity']
                cart_product.total = product.price * decimal.Decimal(request.POST['quantity'])
                cart_product.save()
                messages.info(request, f"{product.name} quantity changed to {cart_product.quantity}")
    return redirect(cartView)

#place order
def place_order(request):
    if request.user.is_staff or request.user.groups.filter(name='Dealers').exists():
        if request.method == 'POST':
            new_order = Order.objects.create(
                bill_to=request.POST['bill_to'],
                ship_to=request.POST['ship_to'],
                shipping=request.POST['shipping'],
                terms=request.POST['terms'],
                po_box=request.POST['po_box'],
                rep=request.POST['rep'],
                comments=request.POST['comments'],
                user=request.user
                )
            cart = Cart.objects.get(user=request.user)
            for item in cart.products.all():
                cart.products.remove(item)
                cart.save()
                new_order.products.add(item)
                new_order.save()
            
            #order info for html
            series = ProductSeries.objects.all()
            musway = series.filter(name='Musway DSP')
            if musway:
                musway = ProductSeries.objects.get(name='Musway DSP')
            musway_total = round(decimal.Decimal(0.00), 2)
            order_total = round(decimal.Decimal(0.00), 2)
            for s in series:
                sum = 0
                msum = 0
                for item in new_order.products.all():
                    if item.series == s:
                        sum += item.total
                    if item.series == musway:
                        msum += item.total
                s.total = round(decimal.Decimal(sum), 2)
                order_total += sum
                musway_total += msum
            aunex_total = order_total - musway_total
            context = {
                "series": series,
                "order": new_order,
                "order_total": order_total,
                "aunex_total": aunex_total,
                "musway_total": musway_total
            }
            
            #send order to email
            subject, from_email, to = f'Order from {request.user.username}', f'Aunex <{settings.EMAIL_HOST_USER}>', settings.EMAIL_ORDER_RECIPIENTS
            html_content = render_to_string('catalogue/email.html', context)
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.info(request, f"Order has been placed successfully.")
            return redirect(f'/products/order/{new_order.id}')
    return redirect(cartView)

#media assets
@login_required
def mediaAssets(request):
    products = Product.objects.all()
    search_media = ''
    if 'search_media' in request.GET:
        search_media = request.GET['search_media']
        products = Product.objects.filter(name__icontains=search_media)
    images = Image.objects.filter(productImage=None, gallery=None, specSheet=None)
    videos = Video.objects.all()
    context = {
        "products": products,
        "images": images,
        "videos": videos,
        "search_media": search_media
    }
    return render(request, "catalogue/media.html", context)

@login_required
def uploadDealers(request):
    #only staff should be able to access this page
    if request.user.is_staff or request.user.groups.filter(name='Dealer Manager').exists():
        if request.method == "POST":
            try:
                csv_file = request.FILES["csv_file"]
                if not csv_file.name.endswith('.csv'):
                    messages.error(request,'File is not CSV type')
                    return redirect(newDealer)
                #if file is too large, return
                if csv_file.multiple_chunks():
                    messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
                    return redirect(newDealer)

                file_data = csv_file.read().decode("utf-8")		

                lines = file_data.split("\n")
                next(iter(lines))
                #loop over the lines and save them in db. If error , store as string and then display
                for line in lines:						
                    fields = line.split(",")
                    data_dict = {}
                    data_dict["name"] = fields[0]
                    data_dict["telephone"] = fields[1]
                    data_dict["address"] = fields[2]
                    data_dict["city"] = fields[3]
                    data_dict["state"] = fields[4]
                    data_dict["zipcode"] = fields[5]
                    data_dict["website"] = fields[6]
                    data_dict["brand"] = fields[7]
                    data_dict["elite"] = fields[8]
                    try:
                        form = DealerForm(data_dict)
                        if form.is_valid():
                            form.save()
                        else:
                            print('Invalid entry')

                    except Exception as e:
                        pass
                
                if LastUpdate.objects.filter(name='Dealers').exists():
                    last_update = LastUpdate.objects.get(name='Dealers')
                    last_update.username = request.user.username
                    last_update.save()
                else:
                    last_update = LastUpdate.objects.create(name='Dealers', username=request.user.username)
                
                messages.info(request, "File uploaded successfully.")

            except Exception as e:
                messages.error(request,"Unable to upload file. "+repr(e))
    
    return redirect(newDealer)

@login_required
def updateDealers(request):
    #only staff should be able to access this page
    if request.user.is_staff or request.user.groups.filter(name='Dealer Manager').exists():
        if request.method == "POST":
            dealers = Dealer.objects.all()
            if dealers:
                for dealer in dealers:

                    try:
                        address = f'{dealer.address} {dealer.city}, {dealer.state} {dealer.zipcode}'
                        req = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + address + '&key=AIzaSyC0uC2V-60qNc3TeAyTtemqebljrdni97A')
                        res = req.json()
                        result = res['results'][0:1]
                        geodata = dict()
                        geodata['lat'] = result[0]['geometry']['location']['lat']
                        geodata['lng'] = result[0]['geometry']['location']['lng']
                        lat = decimal.Decimal('{lat}'.format(**geodata))
                        lng = decimal.Decimal('{lng}'.format(**geodata))
                        dealer.latitude = lat
                        dealer.longitude = lng
                        dealer.save()
                    
                    except:
                        messages.error(request, f"Could not find geodata for {dealer.name}, {address}.")
                        pass
            
            else:
                messages.error(request, "Please upload a .csv file to update dealer locations.")
                return redirect(newDealer)
    
    if LastUpdate.objects.filter(name='Dealers').exists():
        last_update = LastUpdate.objects.get(name='Dealers')
        last_update.username = request.user.username
        last_update.save()
    else:
        last_update = LastUpdate.objects.create(name='Dealers', username=request.user.username)
    
    messages.info(request, "Dealer locations successfully updated.")

    return redirect(newDealer)

@login_required
def updateInventory(request):
    #only staff should be able to access this page
    if request.user.is_staff or request.user.groups.filter(name='Inventory Manager').exists():
        if request.method == "POST":
            try:
                csv_file = request.FILES["csv_file"]
                if not csv_file.name.endswith('.csv'):
                    messages.error(request,'File is not CSV type')
                    return redirect(inventory)
                #if file is too large, return
                if csv_file.multiple_chunks():
                    messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
                    return redirect(inventory)

                file_data = csv_file.read().decode("utf-8")

                lines = file_data.split("\n")
                next(iter(lines))
                #loop over the lines and save them in db. If error , store as string and then display
                for line in lines:
                    fields = line.split(",")
                    stock = Product.objects.all()
                    for item in stock:
                        if fields[0] in item.name:
                            try:
                                item.quantity = fields[1]
                                item.save()
                            except:
                                pass
                
                if LastUpdate.objects.filter(name='Inventory').exists():
                    last_update = LastUpdate.objects.get(name='Inventory')
                    last_update.username = request.user.username
                    last_update.save()
                else:
                    last_update = LastUpdate.objects.create(name='Inventory', username=request.user.username)
                
                messages.info(request, "Inventory updated successfully.")

            except Exception as e:
                messages.error(request,"Unable to upload file. "+repr(e))
    
    return redirect(inventory)