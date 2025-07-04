from django.shortcuts import render
from rest_framework import viewsets, generics
# from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .models import Blueprint, BlueprintItem, ManufacturePlan, ManufacturePlanItem, ManufactureResource, Material, MaterialSubType, MaterialType, Shipment, ShipmentItem, MaterialVariant, Stock, SalePlace, SaleTransaction, ResourcePlan

from .serializers import BlueprintItemSerializer, BlueprintSerializer, ManufacturePlanItemSerializer, ManufacturePlanSerializer, ManufactureResourceSerializer, MaterialSerializer, MaterialSubTypeSerializer, MaterialTypeSerializer, ShipmentItemSerializer, ShipmentSerializer, UserSerializer, MaterialVariantSerializer, StockSerializer, SalePlaceSerializer, SaleTransactionSerializer, ResourcePlanSerializer, UserRegisterSerializer


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    Base viewset with common settings for all model viewsets.
    """
    # pagination_class = PageNumberPagination
    # pagination_class.page_size = 10
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated]


class MaterialTypeViewSet(BaseModelViewSet):
    queryset = MaterialType.objects.all()
    serializer_class = MaterialTypeSerializer


class BlueprintViewSet(BaseModelViewSet):
    queryset = Blueprint.objects.all()
    serializer_class = BlueprintSerializer


class MaterialViewSet(BaseModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class BlueprintItemViewSet(BaseModelViewSet):
    queryset = BlueprintItem.objects.all()
    serializer_class = BlueprintItemSerializer


class MaterialSubTypeViewSet(BaseModelViewSet):
    queryset = MaterialSubType.objects.all()
    serializer_class = MaterialSubTypeSerializer


class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class ShipmentViewSet(BaseModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer


class ShipmentItemViewSet(BaseModelViewSet):
    queryset = ShipmentItem.objects.all()
    serializer_class = ShipmentItemSerializer


class ManufactureResourceViewSet(BaseModelViewSet):
    queryset = ManufactureResource.objects.all()
    serializer_class = ManufactureResourceSerializer


class ManufacturePlanViewSet(BaseModelViewSet):
    queryset = ManufacturePlan.objects.all()
    serializer_class = ManufacturePlanSerializer


class ManufacturePlanItemViewSet(BaseModelViewSet):
    queryset = ManufacturePlanItem.objects.all()
    serializer_class = ManufacturePlanItemSerializer


class MaterialVariantViewSet(BaseModelViewSet):
    queryset = MaterialVariant.objects.all()
    serializer_class = MaterialVariantSerializer


class StockViewSet(BaseModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class SalePlaceViewSet(BaseModelViewSet):
    queryset = SalePlace.objects.all()
    serializer_class = SalePlaceSerializer


class SaleTransactionViewSet(BaseModelViewSet):
    queryset = SaleTransaction.objects.all()
    serializer_class = SaleTransactionSerializer


class ResourcePlanViewSet(BaseModelViewSet):
    queryset = ResourcePlan.objects.all()
    serializer_class = ResourcePlanSerializer


class UserRegisterView(generics.CreateAPIView):
    """
    API view to register a new user.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def get(self, request, *args, **kwargs):
        from rest_framework.response import Response
        from rest_framework import status
        return Response({"detail": "Method \"GET\" not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
