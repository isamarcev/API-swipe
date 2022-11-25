from drf_psq import Rule, PsqMixin

from django.db.models import Max
from django.shortcuts import render, get_object_or_404

from drf_spectacular.utils import extend_schema

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from content import models, serializers
from content.permissions import IsComplexOwner, IsApartmentOwner
from users.permissions import IsDeveloperUser
from content.services.service_serializer import create_related_object
from users.serializers import UserSerializer


@extend_schema(tags=["complex"])
class ComplexViewSet(PsqMixin, viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializers.ComplexSerializer
    queryset = models.Complex.objects.all().\
        prefetch_related('complex_documents', 'complex_images',
                         'complex_news', 'complex_corpus')
    http_method_names = ['get', "post", "put", "delete"]

    # psq_rules = {
    #     'create': [
    #         Rule([IsAdminUser], serializers.ComplexCreateSerializer),
    #         Rule([IsDeveloperUser], serializers.ComplexCreateSerializer)
    #     ],
    #     ('update', 'partial_update', 'destroy'): [
    #         Rule([IsAdminUser], serializers.ComplexCreateSerializer),
    #         Rule([IsComplexOwner], serializers.ComplexCreateSerializer)
    #     ]
    # }

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
        return Response(serializer.data)

    @extend_schema(tags=["add_to_favourite"],
                   request=serializers.serializers.Serializer)
    @action(detail=True, name='add_complex_to_favourite', methods=["put"])
    def add_complex_to_favourite(self, request, *args, **kwargs):
        complex_obj = self.get_object()
        if complex_obj in request.user.favourite_complex.all():
            request.user.favourite_complex.remove(complex_obj)
            return Response("Удалено")
        request.user.favourite_complex.add(complex_obj)
        return Response("Добавлено")


@extend_schema(tags=["complex_document"])
class ComplexDocumentsViewSet(viewsets.ModelViewSet):
    queryset = models.ComplexDocument.objects.all()
    serializer_class = serializers.ComplexDocumentSerializer
    parser_classes = [MultiPartParser]
    http_method_names = ('put', 'post', 'delete')
    permission_classes = [IsComplexOwner, IsAdminUser]

    def create(self, request, *args, **kwargs):
        return create_related_object(self, request, *args, **kwargs)


# @extend_schema(tags=["apartment_image"])
# class ApartmentImageViewSet(viewsets.ModelViewSet):
#     queryset = models.ApartmentImage.objects.all()
#     serializer_class = serializers.ApartmentImageSerializer
#     parser_classes = [MultiPartParser]
#     http_method_names = ('put', 'post', 'delete')
#     permission_classes = [IsApartmentOwner, IsAdminUser]
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'user': request.user})
#         serializer.is_valid(raise_exception=True)
#         apartment = models.Complex.objects.get(pk=request.data['apartment'])
#         serializer.save(apartment=apartment)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


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
    # http_method_names = ('get', 'put', 'post', 'patch', 'delete')
    # parser_classes = [JSONParser]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        apartment_obj = self.get_object()
        serializer = self.get_serializer(apartment_obj)
        return Response(serializer.data)

    @extend_schema(tags=["add_to_favourite"],
                   request=serializers.serializers.Serializer)
    @action(detail=True, name='add_flat_to_favourite', methods=["put"])
    def add_flat_to_favourite(self, request, *args, **kwargs):
        apartment = self.get_object()
        if apartment in request.user.favourite_apartment.all():
            request.user.favourite_apartment.remove(apartment)
            return Response("Удалено")
        request.user.favourite_apartment.add(apartment)
        return Response("Добавлено")


@extend_schema(tags=["moderation"])
class ApartmentModerationViewSet(viewsets.ModelViewSet):
    queryset = models.Apartment.objects.filter(is_moderated=False)
    serializer_class = serializers.ApartmentModerationList

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(is_moderated=False)
        serializer = serializers.ApartmentModerationList(
            queryset, many=True
        )
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        apartment_obj = self.get_object()
            # get_object_or_404(
            # models.Apartment.objects.filter(is_moderated=False),
            # pk=pk
        # )
        print(apartment_obj)
        serializer = serializers.ApartmentModerationObject(
            apartment_obj
        )
        return Response(serializer.data)

    @extend_schema(request=serializers.ApartmentModerationObject)
    def update(self, request, *args, **kwargs):
        # apartment_obj = get_object_or_404(
        #     models.Apartment.objects.filter(is_moderated=False),
        #     pk=pk
        # )
        apartment_obj = self.get_object()
        serializer = serializers.ApartmentModerationObject(
            apartment_obj, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    # @action(detail=False, methods=["get"], name="moderation")
    # def moderation(self, request, *args, **kwargs):
    #     queryset = self.get_queryset().filter(is_moderated=False)
    #     serializer = serializers.ApartmentModerationList(
    #         queryset, many=True
    #     )
    #     return Response(serializer.data)

    # @action(detail=True, methods=["get"], name="moderation_apartment")
    # def moderation(self, request, *args, **kwargs):
    #     apartment_obj = get_object_or_404(
    #         models.Apartment.objects.filter(is_moderated=False),
    #         pk=kwargs.get('pk')
    #     )
    #     if request.method == 'GET':
    #         serializer = serializers.ApartmentModerationObject(
    #             apartment_obj
    #         )
    #         return Response(serializer.data)

    # @action(detail=True, methods=['patch'], name="moderation_apartment_put")
    # def moderation_decide(self, request, *args, **kwargs):
    #     apartment_obj = get_object_or_404(
    #         models.Apartment.objects.filter(is_moderated=False),
    #         pk=kwargs.get('pk')
    #     )
    #     serializer = serializers.ApartmentModerationObject(
    #         apartment_obj
    #     )
    #     return Response(serializer.data)


@extend_schema(tags=["advertisement"])
class AdvertisementViewSer(viewsets.ModelViewSet):
    queryset = models.Advertisement.objects.all()
    serializer_class = serializers.AdvertisementSerializer
    # http_method_names = ["get", "put", "delete"]
    lookup_field = 'apartment'

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["complaint"])
class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = models.Complaint.objects.all()
    serializer_class = serializers.ComplaintSerializer
    http_method_names = ["get", "post", "put", "delete"]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        complaint_obj = self.get_object()
        complaint_obj.is_reviewed = True
        complaint_obj.save()
        serializer = self.get_serializer(complaint_obj)
        return Response(serializer.data)


@extend_schema(tags=["all_feed"])
class AllComplexAndApartmentView(mixins.ListModelMixin,
                                 mixins.UpdateModelMixin,
                                 viewsets.GenericViewSet):

    def list(self, request, *args, **kwargs):
        complex_obj = models.Complex.objects.all()
        apartment = models.Apartment.objects.all()
        serializer = serializers.ComplexRestrictedSerializer(
            complex_obj, many=True)
        serializer_flat = serializers.ApartmentRestrictedSerializer(apartment,
                                                                    many=True)
        return Response({'flats': serializer_flat.data,
                         'complex': serializer.data})





