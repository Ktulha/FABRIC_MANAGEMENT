from rest_framework import serializers


from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class SaleObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleObject
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'

    def create(self, validated_data):
        date = validated_data.pop('date')
        region = validated_data.pop('region')
        sale_object = validated_data.pop('sale_object')
        product = validated_data.pop('product')
        quantity = validated_data.pop('quantity')
        sale, created = Sale.objects.get_or_create(
            date=date, region=region, sale_object=sale_object, product=product,)

        sale.quantity = quantity
        sale.save()
        return sale
