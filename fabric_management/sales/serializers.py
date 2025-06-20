from rest_framework import serializers


from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        name = validated_data.pop('name')
        description = validated_data.pop('description')
        image = validated_data.pop('image')
        url = validated_data.pop('url')
        barcode = validated_data.pop('barcode')
        product, created = Product.objects.get_or_create(
            name=name, barcode=barcode
        )
        product.description = description
        product.image = image
        product.url = url
        product.save()
        return product


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
