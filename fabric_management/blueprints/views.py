from django.shortcuts import render

from rest_framework import viewsets, generics
# from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from blueprints.models import *
from blueprints.serializers import *


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    Base viewset with common settings for all model viewsets.
    """
    # pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [AllowAny]

# Create your views here.


class UnitViewSet(BaseModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class MaterialViewSet(BaseModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class BlueprintViewSet(BaseModelViewSet):
    queryset = Blueprint.objects.all()
    serializer_class = BlueprintSerializer


class BlueprintItemViewSet(BaseModelViewSet):
    queryset = BlueprintItem.objects.all()
    serializer_class = BlueprintItemSerializer
