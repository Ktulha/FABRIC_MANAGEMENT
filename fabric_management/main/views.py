import datetime
from os import name
from django.shortcuts import render
import csv
import json
from django.shortcuts import render
from django.http import HttpResponse

from warehouse.models import StockTransaction, Warehouse
from sales.models import Product, Region, Sale, SaleObject


def index(request):
    return render(request, 'index.html')


def load_sales(request):
    if request.method == 'POST':
        file = request.FILES['file']
        if file.name.endswith('.csv'):
            decoded_file = file.read().decode('utf-8-sig').splitlines()

            reader = csv.DictReader(decoded_file)
            # reader = csv.reader(decoded_file)
            print(reader)
            for row in reader:

                keys = list(row.keys())[0].split(';')
                # print(keys)
                values = list(row.values())[0].split(';')
                # print(values)
                d = dict(zip(keys, values))

                # fill values
                sale_object = d['sale_object']
                region = d['region']
                region_code = d['region_code']
                product = d['product']
                product_barcode = d['product_barcode']
                date = datetime.datetime.strptime(d['date'], '%d.%m.%Y').date()
                quantity = d['quantity']

                # print(sale_object, region, region_code,
                #   product, product_barcode, date, quantity)
                # prod, created = Product.objects.get_or_create(
                #     barcode=product_barcode)
                # print(prod)

                # product
                prod, created = Product.objects.get_or_create(
                    barcode=product_barcode)
                if not prod:
                    prod = Product.objects.create(
                        barcode=product_barcode, name=product)
                prod.name = product
                prod.save()

                # region
                reg, created = Region.objects.get_or_create(code=region_code)
                if not reg:
                    reg = Region.objects.create(
                        name=region, code=region_code)
                reg.name = region
                reg.save()
                # sale object
                sale_obj, created = SaleObject.objects.get_or_create(
                    name=sale_object)
                if not sale_obj:
                    sale_obj = SaleObject.objects.create(
                        name=sale_object)
                sale_obj.name = sale_object
                sale_obj.save()
                # sale
                sale, ceated = Sale.objects.get_or_create(
                    date=date, region=reg, product=prod, sale_object=sale_obj)
                if not sale:
                    sale = Sale.objects.create(
                        date=date, region=reg, product=prod, sale_object=sale_obj, quantity=quantity)

                sale.quantity = quantity
                sale.save()

        elif file.name.endswith('.json'):
            # TODO JSON format data file load script
            pass

        else:
            return HttpResponse('Unsupported file format')
        # HttpResponse('Data loaded successfully')
        return render(request, 'index.html')
    return render(request, 'load_sales.html')


def load_stock(request):
    if request.method == 'POST':
        file = request.FILES['file']
        if file.name.endswith('.csv'):
            decoded_file = file.read().decode('utf-8-sig').splitlines()

            reader = csv.DictReader(decoded_file)

            for row in reader:
                keys = list(row.keys())[0].split(';')
                # print(keys)
                values = list(row.values())[0].split(';')
                # print(values)
                d = dict(zip(keys, values))
                stock_date = datetime.datetime.strptime(
                    d['stock_date'], '%d.%m.%Y').date()
                product_barcode = d['product_barcode']
                product = d['product']
                region = d['region']
                region_code = d['region_code']
                warehouse = d['warehouse']
                warehouse_code = d['warehouse_code']
                quantity = d['quantity']

                # product
                prod, created = Product.objects.get_or_create(
                    barcode=product_barcode)
                if not prod:
                    prod = Product.objects.create(
                        barcode=product_barcode, name=product)
                prod.name = product
                prod.save()

                # region
                reg, created = Region.objects.get_or_create(code=region_code)
                if not reg:
                    reg = Region.objects.create(
                        name=region, code=region_code)
                reg.name = region
                reg.save()
                # warehouse
                ware, created = Warehouse.objects.get_or_create(
                    code=warehouse_code)
                if not ware:
                    ware = Warehouse.objects.create(
                        name=warehouse, code=warehouse_code)
                ware.name = warehouse
                ware.region = reg
                ware.save()

                # stock transactions
                stock_transaction, created = StockTransaction.objects.get_or_create(
                    stock_date=stock_date, product=prod, warehouse=ware)
                if not stock_transaction:
                    stock_transaction = StockTransaction.objects.create(
                        stock_date=stock_date, product=prod, warehouse=ware, quantity=quantity)
                stock_transaction.quantity = quantity
                stock_transaction.save()

        else:
            return HttpResponse('Unsupported file format')
        # HttpResponse('Data loaded successfully')
        return render(request, 'index.html')
    return render(request, 'load_stock.html')
