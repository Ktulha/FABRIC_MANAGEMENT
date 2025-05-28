from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Новые таблицы
SHIPMENT_STATUSES = [('pending', 'PENDING'), ('transit', 'TRANSIT'), ('custom', 'CUSTOM'), (
    'receiving', 'RECEIVING'), ('complete', 'COMPLETE'), ('exception', 'EXCEPTION'), ('failure', 'FAILURE')]

SUPPLEMENT_METHODS = [('production', 'PRODUCTION'), ('buy', 'BUY')]

PRIORITY_LIST = [('alarm', 'ALARM'), ('hight', 'HIGHT'), (
    'medium', 'MEDIUM'), ('low', 'LOW'), ('sometime', 'SOMETIME LATER')]


class ManufactureResource(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    work_slot_count = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Manufacture Resource'
        verbose_name_plural = 'Manufacture Resources'


class MaterialType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'Type:{self.name}'


class MaterialSubType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    material_type = models.ForeignKey(
        MaterialType, related_name='subtypes', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.material_type}=>{self.name}'


class Blueprint(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_result = models.BooleanField(default=False)
    average_execution_time = models.TimeField(
        auto_now=False, auto_now_add=False, null=True)
    minimal_day_production = models.PositiveIntegerField(default=0)
    max_day_production = models.PositiveIntegerField(default=1)
    resource = models.ForeignKey(
        ManufactureResource, related_name='blueprints', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Blueprint:{self.name}'


class Material(models.Model):
    BUY = 'buy'
    PRODUCTION = 'production'
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    blueprint = models.ForeignKey(
        Blueprint, related_name='materials', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='material_img/')
    barcode = models.CharField(max_length=128, blank=True, unique=True)
    material_type = models.ForeignKey(
        MaterialType, related_name='materials', on_delete=models.SET_NULL, null=True)
    material_sub_type = models.ForeignKey(
        MaterialSubType, related_name='materials', on_delete=models.SET_NULL, null=True)
    is_product = models.BooleanField(default=False)
    supplement_method = models.CharField(
        max_length=50, choices=SUPPLEMENT_METHODS, default='buy')

    def save(self, *args, **kwargs):
        if self.barcode:
            self.is_product = True

        if self.blueprint:
            self.supplement_method = self.PRODUCTION
        if self.material_sub_type.material_type != self.material_type:
            raise ValueError('Material type and sub type must be same')
        if self.material_sub_type:
            self.material_type = self.material_sub_type.material_type
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}:{self.barcode}:{self.blueprint}'


class BlueprintItem(models.Model):
    blueprint = models.ForeignKey(
        Blueprint, related_name='items', on_delete=models.CASCADE)
    material = models.ForeignKey(
        Material, related_name='items', on_delete=models.CASCADE)
    amount = models.FloatField(default=0)

    class Meta:
        unique_together = ('blueprint', 'material')

    def save(self, *args, **kwargs):
        if self.amount < 0:
            raise ValueError('Amount cannot be negative')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.material}:{self.amount}'


class Shipment(models.Model):
    shipment_number = models.CharField(max_length=255)
    shipment_date = models.DateField(auto_now=False, auto_now_add=False)
    shipment_status = models.CharField(
        max_length=255, choices=SHIPMENT_STATUSES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,  on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Shipment:{self.shipment_number}'


class ShipmentItem(models.Model):
    shipment = models.ForeignKey(
        Shipment, related_name='items', on_delete=models.CASCADE)
    material = models.ForeignKey(
        Material, related_name='shipment_items', on_delete=models.CASCADE)
    amount = models.FloatField(default=0)

    class Meta:
        unique_together = ('shipment', 'material')


class ManufacturePlan(models.Model):
    date = models.DateField(
        auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,  on_delete=models.SET_NULL, null=True)


class ManufacturePlanItem(models.Model):
    manufacture_plan = models.ForeignKey(
        ManufacturePlan, related_name='items', on_delete=models.CASCADE)
    material = models.ForeignKey(
        Material, related_name='manufacture_plan_items', on_delete=models.CASCADE)
    blueprint = models.ForeignKey(
        Blueprint, related_name='manufacture_plan_items', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    resource = models.ForeignKey(
        ManufactureResource, related_name='manufacture_plan_items', on_delete=models.SET_NULL, null=True)
    extra_slot = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=50, choices=PRIORITY_LIST, default='low')

    class Meta:
        unique_together = ('manufacture_plan', 'material', 'blueprint')

    def save(self, *args, **kwargs):
        if self.material.blueprint != self.blueprint:
            raise ValueError('Wrong blueprint for material')
        if self.blueprint:
            for item in self.blueprint.items:
                if item.material.blueprint:
                    bp, created = ManufacturePlanItem.objects.get_or_create(
                        manufacture_plan=self.manufacture_plan,
                        material=item.material,
                        blueprint=item.blueprint
                    )
                    bp.amount += self.amount*item.amount
                    if not bp.priority:
                        bp.priority = self.priority
                    bp.save()

        super().save(*args, **kwargs)
