from django.shortcuts import render

from django.forms import ModelForm
from catalogue.models import Image, Product, ProductSeries, ProductType, Category, Manual

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

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
