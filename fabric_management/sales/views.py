from django.shortcuts import render
from rest_framework import viewsets, generics
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .serializers import *
from .models import *

# Create your views here.


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    Base viewset with common settings for all model viewsets.
    """
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [AllowAny]


class ProductViewSet(BaseModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class RegionViewSet(BaseModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class SaleObjectViewSet(BaseModelViewSet):
    queryset = SaleObject.objects.all()
    serializer_class = SaleObjectSerializer


class SaleViewSet(BaseModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
