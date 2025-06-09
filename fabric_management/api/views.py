from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User

from .models import Blueprint, BlueprintItem, ManufacturePlan, ManufacturePlanItem, ManufactureResource, Material, MaterialSubType, MaterialType, Shipment, ShipmentItem

from .serializers import BlueprintItemSerializer, BlueprintSerializer, ManufacturePlanItemSerializer, ManufacturePlanSerializer, ManufactureResourceSerializer, MaterialSerializer, MaterialSubTypeSerializer, MaterialTypeSerializer, ShipmentItemSerializer, ShipmentSerializer, UserSerializer


class MaterialTypeViewSet(viewsets.ModelViewSet):
    queryset = MaterialType.objects.all()
    serializer_class = MaterialTypeSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = []


class BlueprintViewSet(viewsets.ModelViewSet):
    queryset = Blueprint.objects.all()
    serializer_class = BlueprintSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = []


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = []


class BlueprintItemViewSet(viewsets.ModelViewSet):
    queryset = BlueprintItem.objects.all()
    serializer_class = BlueprintItemSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = []


class MaterialSubTypeViewSet(viewsets.ModelViewSet):
    queryset = MaterialSubType.objects.all()
    serializer_class = MaterialSubTypeSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = []


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']


class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = []


class ShipmentItemViewSet(viewsets.ViewSet):
    queryset = ShipmentItem.objects.all()
    serializer_class = ShipmentItemSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = []


class ManufactureResourceViewSet(viewsets.ModelViewSet):
    queryset = ManufactureResource.objects.all()
    serializer_class = ManufactureResourceSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = []


class ManufacturePlanViewSet(viewsets.ModelViewSet):
    queryset = ManufacturePlan.objects.all()
    serializer_class = ManufacturePlanSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = []


class ManufacturePlanItemViewSet(viewsets.ModelViewSet):
    queryset = ManufacturePlanItem.objects.all()
    serializer_class = ManufacturePlanItemSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = []
