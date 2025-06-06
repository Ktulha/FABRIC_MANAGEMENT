from rest_framework.routers import DefaultRouter

from .views import BlueprintItemViewSet, BlueprintViewSet, ManufacturePlanItemViewSet, ManufacturePlanViewSet, ManufactureResourceViewSet, MaterialSubTypeViewSet, MaterialTypeViewSet, MaterialViewSet, ShipmentViewSet, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('material_types', MaterialTypeViewSet)
router.register('material_Sub_types', MaterialSubTypeViewSet)
router.register('blueprint_items', BlueprintItemViewSet)
router.register('materials', MaterialViewSet)
router.register('blueprints', BlueprintViewSet)
router.register('shipments', ShipmentViewSet)
router.register('manufacture_resources', ManufactureResourceViewSet)
router.register('manufacture_plans', ManufacturePlanViewSet)
router.register('manufacture_plan_items', ManufacturePlanItemViewSet)

urlpatterns = [

]

urlpatterns.extend(router.urls)
