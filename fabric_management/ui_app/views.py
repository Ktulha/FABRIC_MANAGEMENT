from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from blueprints.models import *

from .utils import *

from ui_app.forms import ProductEdit

from sales.models import Product

# Create your views here.


def index(request):
    if request.method == 'POST':
        return render(request, 'html/index.html')
    else:
        return render(request, 'html/index.html')


def product_list(request):
    products = Product.objects.all().order_by('name')

    return render(request, 'html/product_list.html', {'products': products})


def tag_products(request, tag):

    products = Product.objects.filter(tags__tag__pk=tag)
    return render(request, 'html/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'html/product_detail.html', {'product': product})


def material_list(request):
    materials = Material.objects.filter(
        item_type='material').order_by('name')
    return render(request, 'html/material_list.html', {'materials': materials})


def material_detail(request, material_id):
    material = Material.objects.get(pk=material_id)
    return render(request, 'html/material_detail.html', {'material': material})
