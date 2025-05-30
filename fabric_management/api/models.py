from django.db import models
from django.contrib.auth.models import User

# Новые таблицы
SHIPMENT_STATUSES = [('pending', 'PENDING'), ('transit', 'TRANSIT'), ('custom', 'CUSTOM'), (
    'receiving', 'RECEIVING'), ('complete', 'COMPLETE'), ('exception', 'EXCEPTION'), ('failure', 'FAILURE')]

SUPPLEMENT_METHODS = [('buy', 'BUY'), ('production', 'PRODUCTION')]

PRIORITY_LIST = [('low', 'LOW'), ('alarm', 'ALARM'), ('high', 'HIGH'), (
    'medium', 'MEDIUM'),  ('sometime', 'SOMETIME LATER')]


class ManufactureResource(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    work_slot_count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Resource:{self.name} slots:{self.work_slot_count}'

    # class Meta:
    #     verbose_name = 'Manufacture Resource'
    #     verbose_name_plural = 'Manufacture Resources'


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

    def save(self, *args, **kwargs):
        if self.material_type:
            t, created = MaterialType.objects.get_or_create(
                name=f'{self.material_type}'
            )
            t.save()
            self.material_type = t
        super().save(*args, **kwargs)

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


class MaterialVariant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Material(models.Model):
    BUY = 'buy'
    PRODUCTION = 'production'
    product_name = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    blueprint = models.OneToOneField(
        Blueprint, related_name='material', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='material_img/')
    barcode = models.CharField(max_length=128, blank=True, unique=True)
    material_type = models.ForeignKey(
        MaterialType, related_name='materials', on_delete=models.SET_NULL, null=True)
    material_sub_type = models.ForeignKey(
        MaterialSubType, related_name='materials', on_delete=models.SET_NULL, null=True)
    material_variant = models.ForeignKey(
        MaterialVariant, related_name='materials', on_delete=models.SET_NULL, null=True)
    is_product = models.BooleanField(default=False)
    supplement_method = models.CharField(
        max_length=50, choices=SUPPLEMENT_METHODS, default='buy')

    def save(self, *args, **kwargs):
        if self.barcode:
            self.is_product = True

        if self.blueprint:
            self.supplement_method = self.PRODUCTION
        if self.material_type and self.material_sub_type:
            # if self.material_sub_type.material_type != self.material_type:
            #     raise ValueError('Material type and sub type must be same')
            if self.material_sub_type:
                self.material_type = self.material_sub_type.material_type
        if self.material_variant:
            mat, created = MaterialVariant.objects.get_or_create(
                name=f'{self.material_variant}'
            )
            mat.save()
            self.material_variant = mat

        self.product_name = self.name
        if self.material_variant:
            self.product_name = f'{self.name}_{self.material_variant}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product_name}:{self.barcode}:{self.blueprint}'


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
        auto_now=False, auto_now_add=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,  on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Date:{self.date}'


class ResourcePlan(models.Model):
    manufacture_plan = models.ForeignKey(
        ManufacturePlan, related_name='resource_plan_items', on_delete=models.CASCADE)
    resource = models.ForeignKey(
        ManufactureResource, related_name='resource_plan_items', on_delete=models.CASCADE)
    slots = models.PositiveIntegerField(default=1)
    extra_slots = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('manufacture_plan', 'resource')


class ManufacturePlanItem(models.Model):
    manufacture_plan = models.ForeignKey(
        ManufacturePlan, related_name='items', on_delete=models.CASCADE)
    material = models.ForeignKey(
        Material, related_name='plan_items', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    extra_slot = models.PositiveIntegerField(default=0)
    priority = models.CharField(
        max_length=50, choices=PRIORITY_LIST, default='medium')

    class Meta:
        unique_together = ('manufacture_plan', 'material')

    def save(self, *args, **kwargs):

        if self.material.blueprint:
            m_bp = self.material.blueprint
            for item in BlueprintItem.objects.filter(blueprint=m_bp):
                if item.material.blueprint:
                    bp, created = ManufacturePlanItem.objects.get_or_create(
                        manufacture_plan=self.manufacture_plan,
                        material=item.material
                    )
                    bp.amount += self.amount*item.amount
                    if not bp.priority:
                        bp.priority = self.priority
                    bp.save()
            if self.material.blueprint.resource:
                res, created = ResourcePlan.objects.get_or_create(
                    manufacture_plan=self.manufacture_plan,
                    resource=self.material.blueprint.resource
                )
                res.slots += 1
                if res.resource.work_slot_count < res.slots:
                    self.extra_slot, res.extra_slots = res.slots-res.resource.work_slot_count

                res.save()

        super().save(*args, **kwargs)
