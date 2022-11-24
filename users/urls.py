from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter
from drf_spectacular.utils import extend_schema
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView




router = DefaultRouter()
router.register(r'user', views.UserUpdateView, basename='user_update')

urlpatterns = [
    path("", include(router.urls))
]

urlpatterns += [
    # DJ REST AUTH auth - URLS
    path("auth/login/", LoginView.as_view(), name="rest_login"),
    path("auth/logout/", LogoutView.as_view(), name="rest_logout"),
    path("registration/", RegisterView.as_view(), name="rest_register"),
]
