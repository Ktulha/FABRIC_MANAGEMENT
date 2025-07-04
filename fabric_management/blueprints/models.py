from django.db import models

from sales.models import Product

# Create your models here.
BLUEPRINT_STATUSES = [('active', 'ACTIVE'), ('inactive',
                                             'INACTIVE'), ('deleted', 'DELETED')]
SUPPLEMENT_METHODS = [('raw', 'RAW'), ('buy', 'BUY'),
                      ('manufactured', 'MANUFACTURED'), ('imported', 'IMPORTED')]
ITEM_TYPES = [('product', 'PRODUCT'), ('material', 'MATERIAL'),
              ('semi-product', 'SEMI-PRODUCT')]


class Unit(models.Model):
    name = models.CharField(max_length=50)


class Material(models.Model):
    product_link = models.ForeignKey(
        Product, related_name='material', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, null=True)
    supplement_method = models.CharField(
        max_length=255, choices=SUPPLEMENT_METHODS, default='raw', null=True)
    item_type = models.CharField(
        max_length=255, choices=ITEM_TYPES, default='material', null=True)
    shipment_period = models.IntegerField(default=0, null=True)
    measure_unit = models.ForeignKey(
        Unit, related_name='material', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_values = models.TextField(null=True)

    def __save__(self, *args, **kwargs):
        if self.pk:
            old_values = Product.objects.get(pk=self.pk)
            self.last_values = f'product_link:{old_values.product_link},name:{old_values.name},supplement_method:{old_values.supplement_method},item_type:{old_values.item_type},shipment_period:{old_values.shipment_period},measure_unit:{old_values.measure_unit}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}-({self.item_type})'


class Blueprint(models.Model):
    name = models.CharField(max_length=255, null=True)
    owner = models.ForeignKey(
        Material, related_name='blueprint', on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(
        auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_values = models.TextField(null=True)

    def __save__(self, *args, **kwargs):
        if self.pk:
            old_values = Blueprint.objects.get(pk=self.pk)
            self.last_values = f'name:{old_values.name},owner:{old_values.owner},description:{old_values.description}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class BlueprintItem(models.Model):
    blueprint = models.ForeignKey(
        Blueprint, related_name='blueprint_items', on_delete=models.CASCADE, null=True)
    material = models.ForeignKey(
        Material, related_name='blueprint_items', on_delete=models.CASCADE, null=True)
    ItemBlueprint = models.ForeignKey(
        Blueprint, on_delete=models.CASCADE, null=True)
    amount = models.FloatField(default=0)
    created_at = models.DateTimeField(
        auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_values = models.TextField(null=True)

    # class Meta:
    #     unique_together = ('blueprint', 'material', 'ItemBlueprint',)

    def __save__(self, *args, **kwargs):
        if self.pk:
            old_values = BlueprintItem.objects.get(pk=self.pk)
            self.last_values = f'blueprint:{old_values.blueprint},material:{old_values.material},material_bp:{old_values.ItemBlueprint},amount:{old_values.amount}'
        super().save(*args, **kwargs)
