from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = []
router = DefaultRouter()
router.register(r'user', views.UserUpdateView, basename='user_update')


urlpatterns += router.urls
