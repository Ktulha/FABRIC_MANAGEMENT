from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Fabric, FabricType, Product, ProductBP, BlueprintFabric, Shipment, ShipmentItem, Stock, Sales


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class FabricTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FabricType
        fields = '__all__'


class FabricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabric
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class BlueprintFabricSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlueprintFabric
        fields = '__all__'


class ProductBPSerializer(serializers.ModelSerializer):
    fabrics = BlueprintFabricSerializer(many=True)

    class Meta:
        model = ProductBP
        fields = fields = '__all__'


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'


class ShipmentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentItem
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'
