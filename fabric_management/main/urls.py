from django.urls import path

from main import views


urlpatterns = [
    path('', views.index, name='home'),
    path('load_sales/', views.load_sales, name='load_sales'),
    path('load_stock/', views.load_stock, name='load_stock'),
]
