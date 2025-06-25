import datetime
from os import name
import csv
import json
from django.shortcuts import render
from django.http import HttpResponse
import numpy as np

from warehouse.models import StockTransaction, Warehouse
from sales.models import Product, Region, Sale, SaleObject


def index(request):
    return render(request, 'index.html')


def load_sales(request):
    if request.method == 'POST':
        file = request.FILES['file']
        if file.name.endswith('.csv'):
            delim = ';'
            decoded_file = file.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(decoded_file, delimiter=delim)

            # Collect data from CSV
            products_data = {}
            regions_data = {}
            sale_objects_data = {}
            sales_data = []

            for row in reader:
                sale_object = row['sale_object']
                region = row['region']
                region_code = row['region_code']
                product = row['product'].replace('\\', '')
                print(product)
                product_barcode = row['product_barcode']
                date = datetime.datetime.strptime(
                    row['date'], '%d.%m.%Y').date()
                quantity = float(row['quantity'].replace(',', '.'))

                if not quantity or quantity == np.nan:
                    quantity = 0
                try:
                    quantity = 0+int(quantity)
                except:
                    quantity = 0

                products_data[product_barcode] = product
                regions_data[region_code] = region
                sale_objects_data[sale_object] = sale_object
                sales_data.append({
                    'date': date,
                    'region_code': region_code,
                    'product_barcode': product_barcode,
                    'sale_object_name': sale_object,
                    'quantity': quantity
                })

            # Bulk get or create Products
            print("Bulk get or create Products")
            existing_products = Product.objects.filter(
                barcode__in=products_data.keys())
            existing_products_dict = {p.barcode: p for p in existing_products}
            products_to_create = []
            for barcode, name in products_data.items():
                if barcode not in existing_products_dict:
                    products_to_create.append(
                        Product(barcode=barcode, name=name))
            Product.objects.bulk_create(products_to_create)
            # Refresh existing_products_dict after bulk_create
            print("Refresh existing_products_dict after bulk_create")
            all_products = Product.objects.filter(
                barcode__in=products_data.keys())
            products_dict = {p.barcode: p for p in all_products}

            # Bulk get or create Regions
            print("Bulk get or create Regions")
            existing_regions = Region.objects.filter(
                code__in=regions_data.keys())
            existing_regions_dict = {r.code: r for r in existing_regions}
            regions_to_create = []
            for code, name in regions_data.items():
                if code not in existing_regions_dict:
                    regions_to_create.append(Region(code=code, name=name))
            Region.objects.bulk_create(regions_to_create)
            # Refresh regions_dict after bulk_create
            print("Refresh regions_dict after bulk_create")
            all_regions = Region.objects.filter(code__in=regions_data.keys())
            regions_dict = {r.code: r for r in all_regions}

            # Bulk get or create SaleObjects
            print("Bulk get or create SaleObjects")
            existing_sale_objects = SaleObject.objects.filter(
                name__in=sale_objects_data.keys())
            existing_sale_objects_dict = {
                so.name: so for so in existing_sale_objects}
            sale_objects_to_create = []
            for name in sale_objects_data.keys():
                if name not in existing_sale_objects_dict:
                    sale_objects_to_create.append(SaleObject(name=name))
            SaleObject.objects.bulk_create(sale_objects_to_create)
            # Refresh sale_objects_dict after bulk_create
            print("Refresh sale_objects_dict after bulk_create")
            all_sale_objects = SaleObject.objects.filter(
                name__in=sale_objects_data.keys())
            sale_objects_dict = {so.name: so for so in all_sale_objects}

            # Prepare sales for bulk create or update
            # Fetch existing sales
            print("Fetch existing sales")
            existing_sales = Sale.objects.filter(
                date__in=[s['date'] for s in sales_data],
                region__code__in=[s['region_code'] for s in sales_data],
                product__barcode__in=[s['product_barcode']
                                      for s in sales_data],
                sale_object__name__in=[s['sale_object_name']
                                       for s in sales_data]
            )
            existing_sales_dict = {}
            for sale in existing_sales:
                key = (sale.date, sale.region.code,
                       sale.product.barcode, sale.sale_object.name)
                existing_sales_dict[key] = sale

            sales_to_create = []
            sales_to_update = []
            for s in sales_data:
                key = (s['date'], s['region_code'],
                       s['product_barcode'], s['sale_object_name'])
                if key in existing_sales_dict:
                    sale_obj = existing_sales_dict[key]
                    sale_obj.quantity = s['quantity']
                    sales_to_update.append(sale_obj)
                else:
                    sales_to_create.append(Sale(
                        date=s['date'],
                        region=regions_dict[s['region_code']],
                        product=products_dict[s['product_barcode']],
                        sale_object=sale_objects_dict[s['sale_object_name']],
                        quantity=s['quantity']
                    ))

            if sales_to_create:
                Sale.objects.bulk_create(sales_to_create)
            if sales_to_update:
                Sale.objects.bulk_update(sales_to_update, ['quantity'])

        elif file.name.endswith('.json'):
            # TODO JSON format data file load script
            pass

        else:
            return HttpResponse('Unsupported file format')
        return render(request, 'index.html')
    return render(request, 'load_sales.html')


def load_stock(request):
    if request.method == 'POST':
        file = request.FILES['file']
        if file.name.endswith('.csv'):
            delim = ';'
            decoded_file = file.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(decoded_file, delimiter=delim)

            # Collect data from CSV
            products_data = {}
            regions_data = {}
            warehouses_data = {}
            stock_transactions_data = []

            for row in reader:
                stock_date = datetime.datetime.strptime(
                    row['stock_date'], '%d.%m.%Y').date()
                product_barcode = row['product_barcode']
                product = row['product']
                region = row['region']
                region_code = row['region_code']
                warehouse = row['warehouse']
                warehouse_code = row['warehouse_code']
                quantity = row['quantity']
                if quantity:
                    quantity = float(row['quantity'].replace(',', '.'))
                else:
                    quantity = 0

                products_data[product_barcode] = product
                regions_data[region_code] = region
                warehouses_data[warehouse_code] = {
                    'name': warehouse,
                    'region_code': region_code
                }
                stock_transactions_data.append({
                    'stock_date': stock_date,
                    'product_barcode': product_barcode,
                    'warehouse_code': warehouse_code,
                    'quantity': quantity
                })

            # Bulk get or create Products
            existing_products = Product.objects.filter(
                barcode__in=products_data.keys())
            existing_products_dict = {p.barcode: p for p in existing_products}
            products_to_create = []
            for barcode, name in products_data.items():
                if barcode not in existing_products_dict:
                    products_to_create.append(
                        Product(barcode=barcode, name=name))
            Product.objects.bulk_create(products_to_create)
            all_products = Product.objects.filter(
                barcode__in=products_data.keys())
            products_dict = {p.barcode: p for p in all_products}

            # Bulk get or create Regions
            existing_regions = Region.objects.filter(
                code__in=regions_data.keys())
            existing_regions_dict = {r.code: r for r in existing_regions}
            regions_to_create = []
            for code, name in regions_data.items():
                if code not in existing_regions_dict:
                    regions_to_create.append(Region(code=code, name=name))
            Region.objects.bulk_create(regions_to_create)
            all_regions = Region.objects.filter(code__in=regions_data.keys())
            regions_dict = {r.code: r for r in all_regions}

            # Bulk get or create Warehouses
            existing_warehouses = Warehouse.objects.filter(
                code__in=warehouses_data.keys())
            existing_warehouses_dict = {w.code: w for w in existing_warehouses}
            warehouses_to_create = []
            for code, data in warehouses_data.items():
                if code not in existing_warehouses_dict:
                    region_obj = regions_dict.get(data['region_code'])
                    warehouses_to_create.append(
                        Warehouse(code=code, name=data['name'], region=region_obj))
            Warehouse.objects.bulk_create(warehouses_to_create)
            all_warehouses = Warehouse.objects.filter(
                code__in=warehouses_data.keys())
            warehouses_dict = {w.code: w for w in all_warehouses}

            # Bulk get or create StockTransactions
            existing_stock_transactions = StockTransaction.objects.filter(
                stock_date__in=[s['stock_date']
                                for s in stock_transactions_data],
                product__barcode__in=[s['product_barcode']
                                      for s in stock_transactions_data],
                warehouse__code__in=[s['warehouse_code']
                                     for s in stock_transactions_data]
            )
            existing_stock_transactions_dict = {}
            for st in existing_stock_transactions:
                key = (st.stock_date, st.product.barcode, st.warehouse.code)
                existing_stock_transactions_dict[key] = st

            stock_transactions_to_create = []
            stock_transactions_to_update = []
            for s in stock_transactions_data:
                key = (s['stock_date'], s['product_barcode'],
                       s['warehouse_code'])
                if key in existing_stock_transactions_dict:
                    st_obj = existing_stock_transactions_dict[key]
                    st_obj.quantity = s['quantity']
                    stock_transactions_to_update.append(st_obj)
                else:
                    stock_transactions_to_create.append(StockTransaction(
                        stock_date=s['stock_date'],
                        product=products_dict[s['product_barcode']],
                        warehouse=warehouses_dict[s['warehouse_code']],
                        quantity=s['quantity']
                    ))

            if stock_transactions_to_create:
                StockTransaction.objects.bulk_create(
                    stock_transactions_to_create)
            if stock_transactions_to_update:
                StockTransaction.objects.bulk_update(
                    stock_transactions_to_update, ['quantity'])

        else:
            return HttpResponse('Unsupported file format')
        return render(request, 'index.html')
    return render(request, 'load_stock.html')
