from .views import *
from django.urls import include, path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('regions', RegionViewSet)
router.register('sale_objects', SaleObjectViewSet)
router.register('sales', SaleViewSet, basename='sales')


urlpatterns = [
]
urlpatterns.extend(router.urls)
