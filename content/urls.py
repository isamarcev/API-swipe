from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'complex', views.ComplexViewSet, basename='complex')
router.register(r'complex_image', views.ComplexImageViewSet,
                basename='complex_image')
router.register(r'complex_news', views.ComplexNewsViewSet,
                basename='complex_news')
router.register(r'complex_document', views.ComplexDocumentsViewSet,
                basename='complex_document')
router.register(r'apartment', views.ApartmentViewSet,
                basename='apartment')
router.register(r'advertisement', views.AdvertisementViewSer,
                basename='apartment_ad'),
router.register(r'complaint', views.ComplaintViewSet, basename='complaint')

urlpatterns = [
    path('feed/', views.AllComplexAndApartmentView.as_view({'get':'list'}))
]

urlpatterns += router.urls
