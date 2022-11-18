from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'complex', views.ComplexViewSet, basename='complex')

urlpatterns = router.urls