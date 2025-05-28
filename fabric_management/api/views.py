from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User

from .models import Blueprint, BlueprintItem, Material, MaterialSubType, MaterialType

from .serializers import BlueprintItemSerializer, BlueprintSerializer, MaterialSerializer, MaterialSubTypeSerializer, MaterialTypeSerializer, UserSerializer


class MaterialTypeViewSet(viewsets.ModelViewSet):
    queryset = MaterialType.objects.all()
    serializer_class = MaterialTypeSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']


class BlueprintViewSet(viewsets.ModelViewSet):
    queryset = Blueprint.objects.all()
    serializer_class = BlueprintSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']


class BlueprintItemViewSet(viewsets.ModelViewSet):
    queryset = BlueprintItem.objects.all()
    serializer_class = BlueprintItemSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']


class MaterialSubTypeViewSet(viewsets.ModelViewSet):
    queryset = MaterialSubType.objects.all()
    serializer_class = MaterialSubTypeSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = []
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']

# from .models import BlueprintFabric, Fabric, FabricType, Product, ProductBP

# from .serializers import BlueprintFabricSerializer, FabricSerializer, FabricTypeSerializer, ProductBPSerializer,  ProductSerializer, UserSerializer

# # Create your views here.


# class FabricTypeViewSet(viewsets.ModelViewSet):
#     queryset = FabricType.objects.all()
#     serializer_class = FabricTypeSerializer
#     pagination_class = None
#     http_method_names = ['get', 'post', 'put', 'delete']


# class FabricViewSet(viewsets.ModelViewSet):
#     queryset = Fabric.objects.all()
#     serializer_class = FabricSerializer
#     pagination_class = None
#     http_method_names = ['get', 'post', 'put', 'delete']


# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     pagination_class = None
#     http_method_names = ['get', 'post', 'put', 'delete']


# class ProductBPViewSet(viewsets.ModelViewSet):
#     queryset = ProductBP.objects.all()
#     serializer_class = ProductBPSerializer
#     pagination_class = None
#     http_method_names = ['get', 'post', 'put', 'delete']


# class BlueprintFabricViewSet(viewsets.ModelViewSet):
#     queryset = BlueprintFabric.objects.all()
#     serializer_class = BlueprintFabricSerializer
