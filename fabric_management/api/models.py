from django.db import models
from django.contrib.auth.models import User


class FabricType(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f'{self.name}'


class Fabric(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True)
    fabric_type = models.ForeignKey(
        FabricType, related_name='fabrics', on_delete=models.RESTRICT)
    width = models.FloatField(default=0)
    image = models.ImageField(upload_to='fabric_img/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True)
    barcode = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class ProductBP(models.Model):
    product = models.ForeignKey(
        Product, related_name='blueprints', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Спецификация к "{self.product}"'


class BlueprintFabric(models.Model):
    blueprint = models.ForeignKey(
        ProductBP, related_name='blueprint_fabrics', on_delete=models.CASCADE)
    fabric = models.ForeignKey(
        Fabric, related_name='blueprint_items', on_delete=models.RESTRICT)
    amount = models.FloatField(default=0)


class Shipment(models.Model):
    date_plan = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    waiting = models.BooleanField()
    date_fact = models.DateField()
    author = models.ForeignKey(
        User, related_name='shipments', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'Поставка {self.date_plan}'


class ShipmentItem(models.Model):
    shipment = models.ForeignKey(
        Shipment, related_name='shipment_items', on_delete=models.CASCADE)
    fabric = models.ForeignKey(
        Fabric, related_name='shipment_items', on_delete=models.RESTRICT)
    amount = models.FloatField(default=0)


class Stock (models.Model):
    fabric = models.ForeignKey(
        Fabric, related_name='stock', on_delete=models.CASCADE)
    start_amount = models.FloatField(default=0)
    sales_amount = models.FloatField(default=0)
    income_amount = models.FloatField(default=0)
    date = models.DateField()


class Sales(models.Model):
    product = models.ForeignKey(
        Product, related_name='sales',  on_delete=models.RESTRICT)
    date = models.DateTimeField()
    amount = models.FloatField(default=0)
