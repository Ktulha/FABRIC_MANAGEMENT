from .views import *
from django.urls import include, path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('units', UnitViewSet)
router.register('materials', MaterialViewSet)
router.register('blueprints', BlueprintViewSet)
router.register('blueprint_items', BlueprintItemViewSet)


urlpatterns = [
]
urlpatterns.extend(router.urls)
