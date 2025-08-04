from .views import *
from sales.views import ProductViewSet, RegionViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('warehouses', WarehouseViewSet)
router.register('stock_transactions', StockTransactionViewSet)
router.register('regions', RegionViewSet)
router.register('products', ProductViewSet)


urlpatterns = [
]
urlpatterns.extend(router.urls)
