from django.urls import path
from ui_app import views


urlpatterns = [
    path('', views.index),
    # path('login/', views.login),
    # path('logout/', views.logout),
    # path('register/', views.register),
    path('products/', views.ProductListView.as_view(), name='products'),

]
