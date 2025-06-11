from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

from .models import Blueprint, BlueprintItem, ManufacturePlan, ManufacturePlanItem, ManufactureResource, Material, MaterialSubType, MaterialType, Shipment, ShipmentItem, MaterialVariant, Stock, SalePlace, SaleTransaction, ResourcePlan


class BlueprintItemSerializer(serializers.ModelSerializer):
    """
    Serializer for BlueprintItem model.
    """
    class Meta:
        model = BlueprintItem
        fields = '__all__'


class BlueprintSerializer(serializers.ModelSerializer):
    """
    Serializer for Blueprint model with nested BlueprintItems.
    """
    items = BlueprintItemSerializer(many=True, read_only=True)

    class Meta:
        model = Blueprint
        fields = '__all__'


class ManufacturePlanItemSerializer(serializers.ModelSerializer):
    """
    Serializer for ManufacturePlanItem model.
    """
    class Meta:
        model = ManufacturePlanItem
        fields = '__all__'

    def create(self, validated_data):
        # Get the necessary data from the validated data
        manufacture_plan = validated_data.pop('manufacture_plan')
        material = validated_data.pop('material')
        amount = validated_data.pop('amount')
        extra_slot = validated_data.pop('extra_slot')
        priority = validated_data.pop('priority')

        # Create the ManufacturePlanItem object
        manufacture_plan_item = ManufacturePlanItem.objects.create(
            manufacture_plan=manufacture_plan,
            material=material,
            amount=amount,
            extra_slot=extra_slot,
            priority=priority
        )

        return manufacture_plan_item


class ManufacturePlanSerializer(serializers.ModelSerializer):
    """
    Serializer for ManufacturePlan model with nested ManufacturePlanItems.
    """
    items = ManufacturePlanItemSerializer(many=True, read_only=True)

    class Meta:
        model = ManufacturePlan
        fields = '__all__'


class ManufactureResourceSerializer(serializers.ModelSerializer):
    """
    Serializer for ManufactureResource model.
    """
    class Meta:
        model = ManufactureResource
        fields = '__all__'


class MaterialTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for MaterialType model.
    """
    class Meta:
        model = MaterialType
        fields = '__all__'


class MaterialSubTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for MaterialSubType model.
    """
    material_type = MaterialTypeSerializer(read_only=True)

    class Meta:
        model = MaterialSubType
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    """
    Serializer for Material model.
    """
    # material_type = MaterialTypeSerializer(read_only=True)
    # material_sub_type = MaterialSubTypeSerializer(read_only=True)
    # blueprint = BlueprintSerializer(read_only=True)

    class Meta:
        model = Material
        fields = '__all__'


class MaterialVariantSerializer(serializers.ModelSerializer):
    """
    Serializer for MaterialVariant model.
    """
    class Meta:
        model = MaterialVariant
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    """
    Serializer for Stock model.
    """
    class Meta:
        model = Stock
        fields = '__all__'


class SalePlaceSerializer(serializers.ModelSerializer):
    """
    Serializer for SalePlace model.
    """
    class Meta:
        model = SalePlace
        fields = '__all__'


class SaleTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for SaleTransaction model.
    """
    class Meta:
        model = SaleTransaction
        fields = '__all__'


class ResourcePlanSerializer(serializers.ModelSerializer):
    """
    Serializer for ResourcePlan model.
    """
    class Meta:
        model = ResourcePlan
        fields = '__all__'


class ShipmentItemSerializer(serializers.ModelSerializer):
    """
    Serializer for ShipmentItem model.
    """
    class Meta:
        model = ShipmentItem
        fields = '__all__'


class ShipmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Shipment model with nested ShipmentItems.
    """
    items = ShipmentItemSerializer(many=True, read_only=True)

    class Meta:
        model = Shipment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for Django User model.
    """
    class Meta:
        model = User
        fields = ('id', 'username')


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
