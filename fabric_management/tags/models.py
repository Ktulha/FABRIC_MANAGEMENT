from django.db import models

from blueprints.models import Material
from sales.models import Product

# Create your models here.


class Tag(models.Model):
    name = models.CharField()

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        if self.name:
            return f'#{self.name}'
        else:
            return 'Тег без названия'


class ProductTag(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['product', 'tag']


class MaterialTag(models.Model):
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['material', 'tag']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
