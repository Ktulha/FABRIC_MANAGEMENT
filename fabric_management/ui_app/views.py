from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView


from ui_app.forms import ProductEdit

from sales.models import Product

# Create your views here.


def index(request):
    if request.method == 'POST':
        return render(request, 'html/index.html')
    else:
        return render(request, 'html/index.html')


def product_list(request):
    products = Product.objects.all()

    return render(request, 'html/product_list.html', {'products': products})


def tag_products(request, tag):

    products = Product.objects.filter(tags__tag__pk=tag)
    return render(request, 'html/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'html/product_detail.html', {'product': product})
