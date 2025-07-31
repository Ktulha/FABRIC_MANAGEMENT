from main import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='home'),
    path('load_sales/', views.load_sales, name='load_sales'),
    path('load_stock/', views.load_stock, name='load_stock'),
    path('load_blueprints/', views.load_blueprints, name='load_blueprints'),
]
