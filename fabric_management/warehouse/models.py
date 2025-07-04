from django.db import models

from sales.models import Product, Region

# Create your models here.


class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f'({self.code}) {self.name}'


class StockTransaction(models.Model):
    stock_date = models.DateField(auto_now_add=False, auto_now=False)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='stocks', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
