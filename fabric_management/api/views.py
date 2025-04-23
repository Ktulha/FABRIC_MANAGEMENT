from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User

from .models import Fabric, FabricType, Product, ProductBP

from .serializers import FabricSerializer, FabricTypeSerializer, ProductBPSerializer,  ProductSerializer, UserSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = []
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']


class FabricTypeViewSet(viewsets.ModelViewSet):
    queryset = FabricType.objects.all()
    serializer_class = FabricTypeSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']


class FabricViewSet(viewsets.ModelViewSet):
    queryset = Fabric.objects.all()
    serializer_class = FabricSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']


class ProductBPViewSet(viewsets.ModelViewSet):
    queryset = ProductBP.objects.all()
    serializer_class = ProductBPSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']
