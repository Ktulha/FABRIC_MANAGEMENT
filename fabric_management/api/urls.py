from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import FabricTypeViewSet, FabricViewSet, ProductBPViewSet, ProductViewSet, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('fabric_types', FabricTypeViewSet)
router.register('fabrics', FabricViewSet)
router.register('products', ProductViewSet)
router.register('blueprints', ProductBPViewSet)

urlpatterns = [

]

urlpatterns.extend(router.urls)
