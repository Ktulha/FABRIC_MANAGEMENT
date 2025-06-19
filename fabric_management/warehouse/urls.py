from rest_framework.routers import DefaultRouter
from django.urls import include, path

from sales.views import ProductViewSet, RegionViewSet

from .views import *


router = DefaultRouter()
router.register('warehouses', WarehouseViewSet)
router.register('stock_transactions', StockTransactionViewSet)
router.register('regions', RegionViewSet)
router.register('products', ProductViewSet)


urlpatterns = [
]
urlpatterns.extend(router.urls)
