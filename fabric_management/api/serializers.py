from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Blueprint, BlueprintItem, ManufacturePlan, ManufacturePlanItem, ManufactureResource, Material, MaterialSubType, MaterialType, Shipment, ShipmentItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class BlueprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blueprint
        fields = '__all__'


class MaterialTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialType
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class BlueprintItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlueprintItem
        fields = '__all__'


class MaterialSubTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialSubType
        fields = '__all__'


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'


class ShipmentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentItem
        fields = '__all__'


class ManufactureResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManufactureResource
        fields = '__all__'


class ManufacturePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManufacturePlan
        fields = '__all__'


class ManufacturePlanItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManufacturePlanItem
        fields = '__all__'
