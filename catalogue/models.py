from os import name
from django.db import models
from django.db.models.deletion import CASCADE
from main.models import User

#database listing for an image
class Image(models.Model):
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"{self.image.name}"
    
    class Meta:
        ordering = ['-pk']

#database listing for a manual
class Manual(models.Model):
    file = models.FileField()

    def __str__(self):
        return f"{self.file.name}"
    
    class Meta:
        ordering = ['-pk']

#individual listing for a product (AE1000.4D, AE1800.4D, etc.)
class Product(models.Model):
    name = models.CharField(primary_key=True, max_length=512)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="productImage")
    gallery = models.ManyToManyField(Image, related_name="gallery", blank=True)
    summary = models.CharField(max_length=2048, blank=True)
    specSheet = models.ForeignKey(Image, null=True, blank=True, on_delete=models.CASCADE, related_name="specSheet")
    file = models.ForeignKey(Manual, null=True, blank=True, on_delete=models.CASCADE, related_name="productManual")
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    weight = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    page_position = models.CharField(max_length=512, blank=True)
    inventory_position = models.CharField(max_length=512, blank=True)
    pop = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        ordering = ['pk']

#a set of related product series (Mobile, Powersport, Marine, etc.)
class Category(models.Model):
    name = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.name}"

#the type of the product (Amplifier, Accessory, etc.)
class ProductType(models.Model):
    name = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.name}"

#a set of related products (AE Series, AMX Series, etc.)
class ProductSeries(models.Model):
    banner = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="banner")
    name = models.CharField(primary_key=True, max_length=512)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="seriesImage")
    products = models.ManyToManyField(Product, related_name="products", blank=True)
    summary = models.CharField(max_length=2048)
    description = models.CharField(max_length=9192)
    category = models.ManyToManyField(Category)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name="type", default=0)
    infoImage = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE, related_name="seriesInfoImage")

    def __str__(self):
        return f"{self.name}"



#rep orders
class CartProduct(models.Model):
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    weight = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    series = models.ForeignKey(ProductSeries, on_delete=models.CASCADE, related_name="cart_products")

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, related_name="cart")

    def __str__(self):
        return f"{self.user.username}"


class Order(models.Model):
    bill_to = models.CharField(max_length=512)
    ship_to = models.CharField(max_length=512)
    shipping = models.CharField(max_length=512)
    terms = models.CharField(max_length=512, blank=True, null=True)
    po_box = models.CharField(max_length=512, blank=True, null=True)
    rep = models.CharField(max_length=512, blank=True, null=True)
    comments = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, related_name="order")

    def __str__(self):
        return f"{self.id} - {self.user.username}"



#dealer locations
class Dealer(models.Model):
    name = models.CharField(primary_key=True, max_length=512)
    telephone = models.CharField(max_length=22, blank=True, null=True)
    address = models.CharField(max_length=512, blank=True, null=True)
    city = models.CharField(max_length=512, blank=True, null=True)
    state = models.CharField(max_length=5, blank=True, null=True)
    zipcode = models.CharField(max_length=7, blank=True, null=True)
    website = models.CharField(max_length=512, blank=True, null=True)
    brand = models.CharField(max_length=512, blank=True, null=True)
    elite = models.CharField(max_length=512, blank=True, null=True)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        ordering = ['pk']

#database listing for a document
class Document(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.name:
            return f"{self.name}"
        else:
            return f"{self.file}"
    
    class Meta:
        ordering = ['-uploaded_at']

#record of last user to make modifications
class LastUpdate(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.username}"
    
    class Meta:
        ordering = ['-updated_at']

class Video(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.file.name} {self.file}"
    
    class Meta:
        ordering = ['-pk']
