from drf_psq import Rule, PsqMixin

from django.db.models import Max
from django.shortcuts import render

from drf_spectacular.utils import extend_schema

from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from content import models, serializers
from content.permissions import IsComplexOwner, IsApartmentOwner
from users.permissions import IsDeveloperUser
from content.services.service_serializer import create_related_object


@extend_schema(tags=["complex"])
class ComplexViewSet(PsqMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ComplexSerializer
    queryset = models.Complex.objects.all()
    parser_classes = [MultiPartParser]
    http_method_names = ['get', "post", "put", "delete"]

    psq_rules = {
        'create': [
            Rule([IsAdminUser], serializers.ComplexCreateSerializer),
            Rule([IsDeveloperUser], serializers.ComplexCreateSerializer)
        ],
        ('update', 'partial_update', 'destroy'): [
            Rule([IsAdminUser], serializers.ComplexCreateSerializer),
            Rule([IsComplexOwner], serializers.ComplexCreateSerializer)
        ]
    }

    def list(self, request, *args, **kwargs):
        queryset = models.Complex.objects.filter(owner_id=request.user.id)
        serializer = serializers.ComplexSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = serializers.ComplexSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        complex_obj = self.get_object()
        serializer = self.get_serializer(complex_obj)
        # complex_max_corpus = models.Apartment.objects.filter(complex=complex_obj). \
        #     aggregate(complex_max_corpus=Max('corpus'))['complex_max_corpus']
        return Response(serializer.data)


@extend_schema(tags=["complex_document"])
class ComplexDocumentsViewSet(viewsets.ModelViewSet):
    queryset = models.ComplexDocument.objects.all()
    serializer_class = serializers.ComplexDocumentSerializer
    parser_classes = [MultiPartParser]
    http_method_names = ('put', 'post', 'delete')
    permission_classes = [IsComplexOwner, IsAdminUser]

    def create(self, request, *args, **kwargs):
        return create_related_object(self, request, *args, **kwargs)


@extend_schema(tags=["complex_image"])
class ComplexImageViewSet(viewsets.ModelViewSet):
    queryset = models.ComplexImage.objects.all()
    serializer_class = serializers.ComplexImageSerializer
    parser_classes = [MultiPartParser]
    http_method_names = ('put', 'post', 'delete')
    permission_classes = [IsDeveloperUser]

    def create(self, request, *args, **kwargs):
        return create_related_object(self, request, *args, **kwargs)


@extend_schema(tags=["complex_news"])
class ComplexNewsViewSet(viewsets.ModelViewSet):
    queryset = models.ComplexNews.objects.all()
    serializer_class = serializers.ComplexNewsSerializer
    http_method_names = ('put', 'post', 'delete')
    permission_classes = [IsDeveloperUser]

    def create(self, request, *args, **kwargs):
        return create_related_object(self, request, *args, **kwargs)


@extend_schema(tags=["apartments"])
class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = models.Apartment.objects.all()
    serializer_class = serializers.ApartmentSerializer
    http_method_names = ('get', 'put', 'post', 'patch', 'delete')
    parser_classes = [MultiPartParser, JSONParser]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        apartment_obj = self.get_object()
        serializer = self.get_serializer(apartment_obj)
        return Response(serializer.data)


