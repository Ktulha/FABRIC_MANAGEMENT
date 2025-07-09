import datetime
from os import name
import csv
import json
from django.shortcuts import render
from django.http import HttpResponse
import numpy as np

from warehouse.models import StockTransaction, Warehouse
from sales.models import Product, Region, Sale, SaleObject
from blueprints.models import *


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
                # print(product)
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
            print(' Sales data loaded successfully')
            return render(request, 'index.html')
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
        print('Stock data loaded successfully')
        return render(request, 'index.html')
    return render(request, 'load_stock.html')


def load_blueprints(request):
    if request.method == 'POST':
        file = request.FILES['file']
        if file.name.endswith('.csv'):
            delim = ';'
            decoded_file = file.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(decoded_file, delimiter=delim)
            units_data = {}
            materials_data = {}
            blueprints_data = {}
            owners_data = {}
            blueprint_items_data = []

            for row in reader:
                unit_name = row['unit']
                owner_name = row['owner']
                blueprint_name = row['blueprint']
                material = row['material']
                barcode = row['barcode']
                quantity = row['quantity']
                material_bp = row['material_bp']
                if material_bp == 'nan':
                    material_bp = None

                if barcode == 'nan':
                    barcode = None
                if barcode:
                    blueprint_name = f'{blueprint_name} ({barcode})'

                # print(unit_name, owner_name, blueprint_name,
                    #   material, barcode, quantity)

                units_data[unit_name] = unit_name

                if owner_name:
                    owners_data[owner_name] = {
                        'owner': owner_name,
                        'barcode': barcode
                    }

                    if owner_name not in materials_data:
                        materials_data[owner_name] = {
                            'name': owner_name, 'product_link': None, 'measure_unit': unit_name}

                    if barcode:
                        # print(owner_name, barcode)
                        product = Product.objects.filter(
                            barcode=barcode).first()

                        if product:
                            materials_data[owner_name].update(
                                {'name': product.name, 'product_link': product})
                        else:
                            product = Product.objects.create(
                                name=owner_name, barcode=barcode)

                if material:
                    if material not in materials_data:
                        materials_data[material] = {
                            'name': material,
                            'product_link': None,
                            'measure_unit': unit_name
                        }

                if blueprint_name:
                    if blueprint_name not in blueprints_data:
                        blueprints_data[blueprint_name] = {
                            'name': blueprint_name,
                            'owner': owner_name,
                            'barcode': barcode
                        }
                    else:
                        if barcode:
                            blueprints_data[blueprint_name].update(
                                {'barcode': barcode})
                if material_bp:
                    if material_bp not in blueprints_data:
                        blueprints_data[material_bp] = {
                            'name': material_bp,
                            'owner': material,
                            'barcode': None
                        }

                blueprint_items_data.append({
                    'blueprint': blueprint_name,
                    'material': material,
                    'material_bp': material_bp,
                    'amount': quantity
                })
            print('file read complete')
            existing_units_dict = {}

            existing_units = Unit.objects.filter(name__in=units_data.keys())
            existing_units_dict = {u.name: u for u in existing_units}

            units_to_create = []
            for unit_name in units_data.keys():
                if unit_name not in existing_units_dict:
                    units_to_create.append(
                        Unit(name=unit_name))
            Unit.objects.bulk_create(units_to_create)
            all_units = Unit.objects.filter(
                name__in=units_data.keys()
            )
            unit_dict = {u.name: u for u in all_units
                         }
            print('units created. To create: ', len(units_to_create))

            existing_materials = Material.objects.filter(
                name__in=materials_data.keys()
            )
            existing_materials_dict = {m.name: m for m in existing_materials}
            materials_to_create = []
            for material_name, data in materials_data.items():
                if material_name not in existing_materials_dict:
                    # print(data)
                    materials_to_create.append(
                        Material(name=data['name'],
                                 product_link=data['product_link'],
                                 measure_unit=unit_dict.get(
                                     data['measure_unit']) if data['measure_unit'] else None
                                 )
                    )
            Material.objects.bulk_create(materials_to_create)
            all_materials = Material.objects.filter(
                name__in=materials_data.keys()
            )
            materials_dict = {
                m.name: m for m in all_materials
            }
            print('materials created. To create: ', len(materials_to_create))

            existing_blueprints = Blueprint.objects.filter(
                name__in=blueprints_data.keys()
            )
            existing_blueprints_dict = {
                b.name: b for b in existing_blueprints
            }
            blueprints_to_create = []
            for blueprint_name, data in blueprints_data.items():
                if blueprint_name not in existing_blueprints_dict:
                    owner_obj = materials_dict.get(data['owner'])
                    # print(data)
                    blueprints_to_create.append(
                        Blueprint(
                            name=blueprint_name,
                            owner=owner_obj,
                            barcode=data['barcode']
                        )
                    )

            Blueprint.objects.bulk_create(
                blueprints_to_create
            )
            all_blueprints = Blueprint.objects.filter(
                name__in=blueprints_data.keys()
            )
            blueprints_dict = {
                b.name: b for b in all_blueprints
            }
            print('blueprints created. To create: ', len(blueprints_to_create))

            existing_blueprint_items = BlueprintItem.objects.filter(
                blueprint__name__in=[i['blueprint']
                                     for i in blueprint_items_data],
                material__name__in=[i['material']
                                    for i in blueprint_items_data],
                ItemBlueprint__name__in=[i['material_bp']
                                         for i in blueprint_items_data],
            )

            existing_blueprint_items_dict = {}

            for b in existing_blueprint_items:
                key = (
                    b.blueprint.name,
                    b.material.name,
                    b.ItemBlueprint.name if b.ItemBlueprint else None,
                )
                existing_blueprint_items_dict[key] = b
            print('existing blueprint items', len(
                existing_blueprint_items_dict))
            blueprint_items_to_create = []
            blueprint_items_to_update = []
            for b in blueprint_items_data:
                key = (
                    b['blueprint'],
                    b['material'],
                    b['material_bp'] if b['material_bp'] else None
                )
                if key in existing_blueprint_items_dict:
                    item_obj = existing_blueprint_items_dict[key]
                    if item_obj.amount != float(b['amount']):
                        item_obj.amount = float(b['amount'])
                        blueprint_items_to_update.append(item_obj)
                else:
                    blueprint_items_to_create.append(
                        BlueprintItem(
                            blueprint=blueprints_dict[b['blueprint']],
                            material=materials_dict[b['material']],
                            ItemBlueprint=blueprints_dict[b['material_bp']
                                                          ] if b['material_bp'] else None,
                            amount=float(b['amount'])
                        )
                    )

            if blueprint_items_to_create:
                BlueprintItem.objects.bulk_create(blueprint_items_to_create)
            if blueprint_items_to_update:
                BlueprintItem.objects.bulk_update(
                    blueprint_items_to_update,
                    ['amount']
                )

        else:
            return HttpResponse('Unsupported file format')
        return render(request, 'index.html')
    return render(request, 'load_blueprints.html')
