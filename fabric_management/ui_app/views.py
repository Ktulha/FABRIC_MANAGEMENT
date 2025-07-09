from itertools import product
from django.shortcuts import render
from django.views.generic import ListView

from blueprints.models import Material
from sales.serializers import ProductSerializer
from sales.models import Product

# Create your views here.


def index(request):
    if request.method == 'POST':
        return render(request, 'html/index.html')
    else:
        return render(request, 'html/index.html')


class ProductListView(ListView):
    queryset = Material.objects.all()
    template_name = 'sales/product_list.html'
