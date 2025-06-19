from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import *

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('regions', RegionViewSet)
router.register('sale_objects', SaleObjectViewSet)
router.register('sales', SaleViewSet)


urlpatterns = [
]
urlpatterns.extend(router.urls)
