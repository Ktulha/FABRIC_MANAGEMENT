from django.db import models
from django.urls import reverse

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products', null=True)
    url = models.CharField(max_length=255, blank=True)
    barcode = models.CharField(max_length=50, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_values = models.TextField(blank=True, editable=False)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Объект уже существует, поэтому мы обновляем его
            old_values = Product.objects.get(pk=self.pk)
            self.last_values = f'name: {old_values.name}, barcode: {old_values.barcode}, description: {old_values.description}, image: {old_values.image}, url: {old_values.url}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}({self.barcode})'

    def get_absolute_url(self):
        return reverse("products", kwargs={"product_id": self.pk})


class Region(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'({self.code}) {self.name}'


class SaleObject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='sale_objects', null=True)

    def __str__(self):
        return self.name


class Sale(models.Model):
    sale_object = models.ForeignKey(SaleObject, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='sales', on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    quantity = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.date}: {self.sale_object.name}({self.region.code}) {self.product.name}({self.quantity})'
