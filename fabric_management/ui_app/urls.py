from ui_app import views
from django.urls import path


urlpatterns = [
    # path('', views.index),
    # path('login/', views.login),
    # path('logout/', views.logout),
    # path('register/', views.register),

    path('', views.product_list, name='products'),
    path('tag_products/<int:tag>/', views.tag_products, name='tag_products'),
    path('products/<int:product_id>/', views.product_detail, name='products'),
    path('materials/', views.material_list, name='materials'),
    # path('blueprints/', views.blueprint_list, name='blueprints'),
    # path('sales/', views.sale_list, name='sales'),
    # path('stock/', views.stock_list, name='stock'),
    path('materials/<int:material_id>/',
         views.material_detail, name='materials'),
    # path('blueprints/<int:pk>/', views.blueprint_detail, name='blueprint_detail'),

]
