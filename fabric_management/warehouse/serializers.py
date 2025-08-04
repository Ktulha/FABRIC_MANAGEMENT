from rest_framework import serializers


from .models import Warehouse,  StockTransaction


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class StockTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransaction
        fields = '__all__'

    def create(self, validated_data):
        stock_date = validated_data.get('stock_date')
        warehouse = validated_data.get('warehouse')
        product = validated_data.get('product')
        s_quantity = validated_data.get('quantity')

        get_transaction, created = StockTransaction.objects.get_or_create(
            stock_date=stock_date,
            warehouse=warehouse,
            product=product,
        )

        get_transaction.quantity = s_quantity
        get_transaction.save()
        return get_transaction
