from django.urls import path
from rest_framework.routers import DefaultRouter

from .models import MaterialType

from .views import BlueprintItemViewSet, BlueprintViewSet, MaterialSubTypeViewSet, MaterialTypeViewSet, MaterialViewSet, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('material_types', MaterialTypeViewSet)
router.register('material_Sub_types', MaterialSubTypeViewSet)
router.register('blueprint_items', BlueprintItemViewSet)
router.register('materials', MaterialViewSet)
router.register('blueprints', BlueprintViewSet)

urlpatterns = [

]

urlpatterns.extend(router.urls)
