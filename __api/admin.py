from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(ManufactureResource)
admin.site.register(MaterialType)
admin.site.register(MaterialSubType)
admin.site.register(Blueprint)
admin.site.register(MaterialVariant)
admin.site.register(Material)
admin.site.register(Stock)
admin.site.register(BlueprintItem)
admin.site.register(Shipment)
admin.site.register(ShipmentItem)
admin.site.register(ManufacturePlan)
admin.site.register(ResourcePlan)
admin.site.register(ManufacturePlanItem)
admin.site.register(SalePlace)
admin.site.register(SaleTransaction)
