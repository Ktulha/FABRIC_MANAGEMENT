from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from sales.serializers import ProductSerializer

from .serializers import WarehouseSerializer, StockTransactionSerializer
from .models import Warehouse, StockTransaction

# Create your views here.


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    Base viewset with common settings for all model viewsets.
    """
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [AllowAny]


class WarehouseViewSet(BaseModelViewSet):
    serializer_class = WarehouseSerializer
    queryset = Warehouse.objects.all()


class StockTransactionViewSet(BaseModelViewSet):
    serializer_class = StockTransactionSerializer
    queryset = StockTransaction.objects.all()
