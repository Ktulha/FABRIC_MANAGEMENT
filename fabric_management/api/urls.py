from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import BlueprintItemViewSet, BlueprintViewSet, ManufacturePlanItemViewSet, ManufacturePlanViewSet, ManufactureResourceViewSet, MaterialSubTypeViewSet, MaterialTypeViewSet, MaterialViewSet, ShipmentItemViewSet, ShipmentViewSet, UserViewSet, MaterialVariantViewSet, StockViewSet, SalePlaceViewSet, SaleTransactionViewSet, ResourcePlanViewSet, UserRegisterView

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('material_types', MaterialTypeViewSet)
router.register('material_sub_types', MaterialSubTypeViewSet)
router.register('blueprint_items', BlueprintItemViewSet)
router.register('materials', MaterialViewSet)
router.register('blueprints', BlueprintViewSet)
router.register('shipments', ShipmentViewSet)
router.register('shipment_items', ShipmentItemViewSet)
router.register('manufacture_resources', ManufactureResourceViewSet)
router.register('manufacture_plans', ManufacturePlanViewSet)
router.register('manufacture_plan_items', ManufacturePlanItemViewSet)
router.register('material_variants', MaterialVariantViewSet)
router.register('stocks', StockViewSet)
router.register('sale_places', SalePlaceViewSet)
router.register('sale_transactions', SaleTransactionViewSet)
router.register('resource_plans', ResourcePlanViewSet)


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),


]

urlpatterns.extend(router.urls)
