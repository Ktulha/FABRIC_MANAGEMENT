from django.db.models import Sum
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Новые таблицы
SHIPMENT_STATUSES = [('pending', 'PENDING'), ('transit', 'TRANSIT'), ('custom', 'CUSTOM'), (
    'receiving', 'RECEIVING'), ('complete', 'COMPLETE'), ('exception', 'EXCEPTION'), ('failure', 'FAILURE')]

SUPPLEMENT_METHODS = [('buy', 'BUY'), ('production', 'PRODUCTION')]

PRIORITY_LIST = [('low', 'НИЗКИЙ'), ('alarm', 'ТРЕВОГА'), ('high', 'ВЫСОКИЙ'), (
    'medium', 'СРЕДНИЙ'),  ('sometime', 'ПОЗЖЕ')]

SALES_OPERATIONS = [('sale', 'ПРОДАЖА'), ('return', 'ВОЗВРАТ')]

PLAN_STATUSES = [('pending', 'В ОЖИДАНИИ'), ('plan', 'ПЛАН'), ('production',
                                                               'ПРОИЗВОДСТВО'), ('completed', 'ЗАВЕРШЕНО'), ('failure', 'ОШИБКА')]


class ManufactureResource(models.Model):
    """
    Модель, представляющая производственный ресурс.

    Атрибуты:
        name (CharField): Название ресурса.
        description (TextField): Описание ресурса.
        created_at (DateTimeField): Дата и время создания записи.
        updated_at (DateTimeField): Дата и время последнего обновления записи.
        work_slot_count (PositiveIntegerField): Количество рабочих слотов.
        minimum_slot_time (TimeField): Минимальное время слота.
        maximum_slot_time (TimeField): Максимальное время слота.

    Методы:
        clean(): Проверяет, что максимальное время слота не меньше минимального.
        save(): Сохраняет объект с валидацией.
        __str__(): Возвращает строковое представление ресурса.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    work_slot_count = models.PositiveIntegerField(default=1)
    minimum_slot_time = models.TimeField(
        auto_now=False, auto_now_add=False, null=True, default=None)
    maximum_slot_time = models.TimeField(
        auto_now=False, auto_now_add=False, null=True, default=None)

    def clean(self):
        if self.maximum_slot_time and self.minimum_slot_time and self.maximum_slot_time < self.minimum_slot_time:
            raise ValidationError(
                'Maximum slot time cannot be less than minimum slot time.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Resource:{self.name} slots:{self.work_slot_count} from {self.minimum_slot_time} to {self.maximum_slot_time}'


class MaterialType(models.Model):
    """
    Модель, представляющая тип материала.

    Атрибуты:
        name (CharField): Название типа материала.
        description (TextField): Описание типа материала.

    Методы:
        __str__(): Возвращает строковое представление типа материала.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'Type:{self.name}'


class MaterialSubType(models.Model):
    """
    Модель, представляющая подтип материала, связанный с типом материала.

    Атрибуты:
        name (CharField): Название подтипа материала.
        description (TextField): Описание подтипа материала.
        material_type (ForeignKey): Внешний ключ на тип материала.

    Методы:
        save(): Обеспечивает корректное сохранение связи с типом материала.
        __str__(): Возвращает строковое представление подтипа материала.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    material_type = models.ForeignKey(
        MaterialType, related_name='subtypes', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Ensure material_type is saved and valid
        if self.material_type_id:
            self.material_type = MaterialType.objects.get(
                id=self.material_type_id)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.material_type}=>{self.name}'


class Blueprint(models.Model):
    """
    Модель, представляющая производственный чертеж (blueprint).

    Атрибуты:
        name (CharField): Название чертежа.
        description (TextField): Описание чертежа.
        created_at (DateTimeField): Дата и время создания.
        updated_at (DateTimeField): Дата и время обновления.
        is_result (BooleanField): Флаг, указывающий, является ли результатом.
        average_execution_time (TimeField): Среднее время выполнения.
        minimal_day_production (PositiveIntegerField): Минимальное дневное производство.
        max_day_production (PositiveIntegerField): Максимальное дневное производство.
        resource (ForeignKey): Внешний ключ на производственный ресурс.

    Методы:
        clean(): Проверяет корректность минимального и максимального производства.
        save(): Сохраняет объект с валидацией и обновляет имя при наличии связанного материала.
        __str__(): Возвращает строковое представление чертежа.
    """
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_result = models.BooleanField(default=False)
    average_execution_time = models.TimeField(null=True)
    minimal_day_production = models.PositiveIntegerField(default=0)
    max_day_production = models.PositiveIntegerField(default=1)
    resource = models.ForeignKey(
        ManufactureResource, related_name='blueprints', on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):

        if hasattr(self, 'material') and self.material:
            self.name = f'({self.material.name})_blueprint'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class MaterialVariant(models.Model):
    """
    Модель, представляющая вариант материала.

    Атрибуты:
        name (CharField): Название варианта.
        created_at (DateTimeField): Дата и время создания.
        updated_at (DateTimeField): Дата и время обновления.

    Методы:
        __str__(): Возвращает строковое представление варианта материала.
    """
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Material(models.Model):
    """
    Модель, представляющая материал с различными атрибутами и связями.

    Атрибуты:
        product_name (CharField): Название продукта, уникальное.
        name (CharField): Название материала.
        description (TextField): Описание материала.
        blueprint (OneToOneField): Связь с чертежом.
        image (ImageField): Изображение материала.
        barcode (CharField): Штрихкод, уникальный.
        material_type (ForeignKey): Внешний ключ на тип материала.
        material_sub_type (ForeignKey): Внешний ключ на подтип материала.
        material_variant (ForeignKey): Внешний ключ на вариант материала.
        is_product (BooleanField): Флаг, указывающий, является ли продуктом.
        supplement_method (CharField): Метод пополнения (покупка или производство).

    Методы:
        save(): Сохраняет объект с валидацией и обновляет поля в зависимости от связей.
        __str__(): Возвращает строковое представление материала.
    """
    BUY = 'buy'
    PRODUCTION = 'production'
    product_name = models.CharField(max_length=255, unique=True, null=True)
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

    # def clean(self):
    #     # Validate that material_type matches material_sub_type's material_type
    #     if self.material_type and self.material_sub_type and self.material_type != self.material_sub_type.material_type:
    #         raise ValidationError(
    #             'Material type must match material sub type\'s material type.')

    def save(self, *args, **kwargs):
        # self.full_clean()
        if self.barcode:
            self.is_product = True

        if self.blueprint:
            self.supplement_method = self.PRODUCTION

        # Ensure material_variant is saved and assigned properly
        if self.material_variant_id:
            self.material_variant = MaterialVariant.objects.get(
                id=self.material_variant_id)

        self.product_name = self.name
        if self.material_variant:
            self.product_name = f'{self.name}_{self.material_variant}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product_name}({self.barcode}):{self.blueprint}'

# для склада


class Stock(models.Model):
    """
    Модель, представляющая складские запасы материала на определенную дату.

    Атрибуты:
        date (DateField): Дата учета.
        material (ForeignKey): Внешний ключ на материал.
        amount (PositiveIntegerField): Количество материала.

    Метаданные:
        unique_together: Уникальность по дате и материалу.
    """
    date = models.DateField(auto_now=False, auto_now_add=False)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('date', 'material')


class BlueprintItem(models.Model):
    """
    Модель, представляющая элемент чертежа с материалом и количеством.

    Атрибуты:
        blueprint (ForeignKey): Внешний ключ на чертеж.
        material (ForeignKey): Внешний ключ на материал.
        amount (FloatField): Количество материала.

    Метаданные:
        unique_together: Уникальность по чертежу и материалу.

    Методы:
        clean(): Проверяет, что количество не отрицательное.
        save(): Сохраняет объект с валидацией.
        __str__(): Возвращает строковое представление элемента.
    """
    blueprint = models.ForeignKey(
        Blueprint, related_name='items', on_delete=models.CASCADE)
    material = models.ForeignKey(
        Material, related_name='items', on_delete=models.CASCADE)
    amount = models.FloatField(default=0)

    class Meta:
        unique_together = ('blueprint', 'material')

    def clean(self):
        if self.amount < 0:
            raise ValidationError('Amount cannot be negative')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.material}:{self.amount}'


class Shipment(models.Model):
    """
    Модель, представляющая отгрузку с информацией о статусе и пользователе.

    Атрибуты:
        shipment_number (CharField): Номер отгрузки.
        shipment_date (DateField): Дата отгрузки.
        shipment_status (CharField): Статус отгрузки.
        created_at (DateTimeField): Дата и время создания записи.
        updated_at (DateTimeField): Дата и время последнего обновления записи.
        user (ForeignKey): Внешний ключ на пользователя, связанного с отгрузкой.

    Методы:
        __str__(): Возвращает строковое представление отгрузки.
    """
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
    """
    Модель, представляющая элемент отгрузки с материалом и количеством.

    Атрибуты:
        shipment (ForeignKey): Внешний ключ на отгрузку.
        material (ForeignKey): Внешний ключ на материал.
        amount (FloatField): Количество материала.

    Метаданные:
        unique_together: Уникальность по отгрузке и материалу.
    """
    shipment = models.ForeignKey(
        Shipment, related_name='items', on_delete=models.CASCADE)
    material = models.ForeignKey(
        Material, related_name='shipment_items', on_delete=models.CASCADE)
    amount = models.FloatField(default=0)

    class Meta:
        unique_together = ('shipment', 'material')


class ManufacturePlan(models.Model):
    """
    Модель, представляющая производственный план на конкретную дату.

    Атрибуты:
        date (DateField): Дата производственного плана.
        created_at (DateTimeField): Дата и время создания записи.
        updated_at (DateTimeField): Дата и время последнего обновления записи.

    Методы:
        __str__(): Возвращает строковое представление даты плана.
    """
    date = models.DateField(
        auto_now=False, auto_now_add=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.date}'


class ResourcePlan(models.Model):
    """
    Модель, представляющая распределение ресурсов в производственном плане.

    Атрибуты:
        manufacture_plan (ForeignKey): Внешний ключ на производственный план.
        resource (ForeignKey): Внешний ключ на производственный ресурс.
        slots (PositiveIntegerField): Количество слотов.
        extra_slots (PositiveIntegerField): Количество дополнительных слотов.

    Метаданные:
        unique_together: Уникальность по производственному плану и ресурсу.
    """
    manufacture_plan = models.ForeignKey(
        ManufacturePlan, related_name='resource_plan_items', on_delete=models.CASCADE)
    resource = models.ForeignKey(
        ManufactureResource, related_name='resource_plan_items', on_delete=models.CASCADE)
    total_slots = models.PositiveIntegerField(default=1)
    used_slots = models.PositiveIntegerField(default=0, null=True)
    extra_slots = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('manufacture_plan', 'resource')

    def save(self, *args, **kwargs):

        self.total_slots = self.resource.work_slot_count
        total_used_slots = self.resource_plan_items.aggregate(
            total=Sum('used_slots'))['total']
        self.used_slots = total_used_slots or 0
        ex_slots = self.used_slots-self.total_slots
        if ex_slots > 0:
            self.extra_slots = ex_slots
        else:
            self.extra_slots = 0
        super().save(*args, **kwargs)


class ManufacturePlanItem(models.Model):
    """
    Модель, представляющая элемент производственного плана с приоритетом и дополнительными слотами.

    Атрибуты:
        manufacture_plan (ForeignKey): Внешний ключ на производственный план.
        material (ForeignKey): Внешний ключ на материал.
        amount (PositiveIntegerField): Количество материала.
        extra_slot (PositiveIntegerField): Количество дополнительных слотов.
        priority (CharField): Приоритет элемента.
        status (CharField): Статус элемента.
        stock_amount (PositiveIntegerField): Количество на складе.

    Метаданные:
        unique_together: Уникальность по производственному плану и материалу.

    Методы:
        save(): Сохраняет объект с учетом связанных элементов и обновляет складские запасы.
        __str__(): Возвращает строковое представление элемента.
    """
    manufacture_plan = models.ForeignKey(
        ManufacturePlan, related_name='items', on_delete=models.CASCADE, null=True)
    material = models.ForeignKey(
        Material, related_name='plan_items', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    extra_slot = models.PositiveIntegerField(default=0, null=True)
    priority = models.CharField(
        max_length=50, choices=PRIORITY_LIST, default='medium')
    status = models.CharField(
        max_length=50, choices=PLAN_STATUSES, default='pending')
    stock_amount = models.PositiveIntegerField(default=0)
    resource_plan = models.ForeignKey(
        ResourcePlan, related_name='resource_plan_items', on_delete=models.SET_NULL, null=True)
    average_time = models.DurationField(null=True)
    used_slots = models.DecimalField(
        max_digits=15, decimal_places=3, default=0)

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
                res.save()
            self.resource_plan = res

            self.average_time = datetime.timedelta(
                seconds=self.material.blueprint.average_execution_time.total_seconds()*self.amount)
            self.used_slots = self.average_time.total_seconds(
            )/self.material.blueprint.resource.maximum_slot_time.total_seconds()
            # Removed recursive save call here

        if self.status == 'finished':
            stock, created = Stock.objects.get_or_create(
                date=self.manufacture_plan.date,
                material=self.material,
            )
            stock.amount += self.amount
            stock.save()
        if not self.manufacture_plan:
            p, created = ManufacturePlan.objects.get_or_create(
                date=datetime.date.today())
            p.save()

            self.manufacture_plan = p

        try:
            s = Stock.objects.get(
                date=self.manufacture_plan.date,
                material=self.material
            )
        except Stock.DoesNotExist:
            s = Stock.objects.create(
                date=self.manufacture_plan.date,
                material=self.material,
                amount=0
            )
        s.save()
        self.stock_amount = s.amount

        super().save(*args, **kwargs)
        if self.amount == 0:
            self.delete()

    def __str__(self):
        return f'{self.material}:{self.amount}'


# продажи

class SalePlace(models.Model):
    """
    Модель, представляющая место продажи.

    Атрибуты:
        name (CharField): Название места продажи.
        description (TextField): Описание места продажи.

    Методы:
        __str__(): Возвращает строковое представление места продажи.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name}'


class SaleTransaction(models.Model):
    """
    Модель, представляющая транзакцию продажи.

    Атрибуты:
        date (DateField): Дата транзакции.
        sale_place (ForeignKey): Внешний ключ на место продажи.
        material (ForeignKey): Внешний ключ на материал.
        amount (PositiveIntegerField): Количество материала.
        operation (CharField): Операция (продажа или возврат).

    Метаданные:
        unique_together: Уникальность по дате, месту продажи и материалу.
    """
    date = models.DateField(auto_now=False, auto_now_add=False)
    sale_place = models.ForeignKey(
        SalePlace, related_name='sale_transactions', on_delete=models.CASCADE)
    material = models.ForeignKey(
        Material, related_name='sale_transactions', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    operation = models.CharField(
        max_length=50, choices=SALES_OPERATIONS, default='sale')

    class Meta:
        unique_together = ('date', 'sale_place', 'material')
