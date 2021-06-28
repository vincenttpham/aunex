from django.db import models
from django.db.models.deletion import CASCADE

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
