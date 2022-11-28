from django.urls import path, include, re_path
from . import views

from rest_framework.routers import DefaultRouter
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from dj_rest_auth.views import \
    (LoginView,
     LogoutView,
     PasswordResetView,
     PasswordResetConfirmView)


router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user_update')
router.register(r'notary', views.NotaryViewSet, basename='notary_viewset')
router.register(r'message', views.MessagesViewSet, basename='message_viewset')

urlpatterns = [
    path("", include(router.urls))
]

urlpatterns += [
    # DJ REST AUTH auth - URLS
    path("auth/login/", LoginView.as_view(), name="rest_login"),
    path("auth/logout/", LogoutView.as_view(), name="rest_logout"),
    path("registration/", RegisterView.as_view(), name="rest_register"),
    path("verify-email/<str:key>/", views.VerifyEmailViewCustom.as_view(),
         name="account_confirm_email"),
    path("account-confirm-email/",
         VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path("password/reset/",
         PasswordResetView.as_view(), name='password_reset'),
    path("password/reset/confirm/<uidb64>/<token>/",
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]

