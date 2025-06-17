# from rest_framework.routers import DefaultRouter
from django.urls import include, path

from datawork import views

# router = DefaultRouter()
urlpatterns = [
    path("", views.index, name="index"),
]
# urlpatterns.extend(router.urls)
