from rest_framework import serializers

from sales.serializers import ProductSerializer
from .models import *


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


class ShortMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'name', 'blueprint', 'measure_unit')


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class ShortBlueprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blueprint
        fields = ('id', 'name')


class BlueprintItemSerializer(serializers.ModelSerializer):
    material = ShortMaterialSerializer(many=False, read_only=True)
    ItemBlueprint = serializers.SerializerMethodField()

    class Meta:
        model = BlueprintItem
        fields = ('id', 'material', 'ItemBlueprint', 'amount')

    def get_ItemBlueprint(self, obj):
        if obj.ItemBlueprint is not None:
            return BlueprintSerializer(obj.ItemBlueprint).data
        return None


class BlueprintSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    owner = ShortMaterialSerializer(many=False, read_only=True)
    blueprint_items = BlueprintItemSerializer(many=True, read_only=True)

    class Meta:
        model = Blueprint
        fields = '__all__'
        depth = 5
