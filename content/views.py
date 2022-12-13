from drf_psq import Rule, PsqMixin

from django.db.models import Q

from django_filters import rest_framework as filters
from .filters import AdvertisementFilter, ApartmentFilter

from drf_spectacular.utils import extend_schema, OpenApiParameter, \
    OpenApiResponse

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from content import models, serializers
from content.permissions import IsComplexOwner, IsApartmentOwner
from users.permissions import IsDeveloperUser
from content.services.service_serializer import create_related_object


@extend_schema(tags=["complex"])
class ComplexViewSet(PsqMixin, viewsets.ModelViewSet):
    serializer_class = serializers.ComplexSerializer
    queryset = models.Complex.objects.all().\
        prefetch_related('complex_documents', 'complex_images',
                         'complex_news', 'complex_corpus')
    http_method_names = ['get', "post", "put", "delete"]

    psq_rules = {
        ('list', 'add_complex_to_favourite', 'retrieve'): [
            Rule([IsAuthenticated]),
        ],
        'create': [
            Rule([IsAdminUser], serializers.ComplexCreateSerializer),
            Rule([IsDeveloperUser], serializers.ComplexCreateSerializer)
        ],
        ('update', 'partial_update', 'destroy'): [
            Rule([IsAdminUser], serializers.ComplexCreateSerializer),
            Rule([IsDeveloperUser], serializers.ComplexCreateSerializer),
            Rule([IsComplexOwner], serializers.ComplexCreateSerializer)
        ],
    }

    @extend_schema(responses={200: OpenApiResponse(
        response=serializers.ComplexRestrictedSerializer
    )})
    def list(self, request, *args, **kwargs):
        queryset = models.Complex.objects.all()
        serializer = serializers.ComplexRestrictedSerializer(queryset,
                                                             many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = serializers.ComplexSerializer(data=request.data,
                                                   context={
                                                       'owner': request.user
                                                   })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        complex_obj = self.get_object()
        serializer = self.get_serializer(complex_obj)
        return Response(serializer.data)

    @extend_schema(tags=["favourites"],
                   request=serializers.serializers.Serializer)
    @action(detail=True, name='add_complex_to_favourite', methods=["put"],)
    def add_complex_to_favourite(self, request, *args, **kwargs):
        complex_obj = self.get_object()
        if complex_obj in request.user.favourite_complex.all():
            request.user.favourite_complex.remove(complex_obj)
            return Response("Удалено")
        request.user.favourite_complex.add(complex_obj)
        return Response("Добавлено")

    @extend_schema(tags=["favourites"],
                   request=serializers.serializers.Serializer,
                   responses={200: OpenApiResponse(
                       response=serializers.ComplexRestrictedSerializer)}
                   )
    @action(detail=False, name='complex_favourite', methods=["get"], )
    def favourites_complex(self, request, *args, **kwargs):
        complexes = request.user.favourite_complex.all()
        serializer = serializers.ComplexRestrictedSerializer(complexes,
                                                             many=True)
        return Response(serializer.data)


@extend_schema(tags=["complex_document"])
class ComplexDocumentsViewSet(PsqMixin, viewsets.ModelViewSet):
    queryset = models.ComplexDocument.objects.all()
    serializer_class = serializers.ComplexDocumentSerializer
    parser_classes = [MultiPartParser]
    http_method_names = ('put', 'post', 'delete')

    psq_rules = {
        'list': [Rule([IsAdminUser])],
        ('create', 'update', 'partial_update', 'destroy'): [
            Rule([IsAdminUser]),
            Rule([IsComplexOwner])
        ],
    }

    def create(self, request, *args, **kwargs):
        return create_related_object(self, request, *args, **kwargs)


@extend_schema(tags=["complex_image"])
class ComplexImageViewSet(viewsets.ModelViewSet):
    queryset = models.ComplexImage.objects.all()
    serializer_class = serializers.ComplexImageSerializer
    parser_classes = [MultiPartParser]
    http_method_names = ('put', 'post', 'delete')
    permission_classes = [IsComplexOwner]

    def create(self, request, *args, **kwargs):
        return create_related_object(self, request, *args, **kwargs)


@extend_schema(tags=["complex_news"])
class ComplexNewsViewSet(viewsets.ModelViewSet):
    queryset = models.ComplexNews.objects.all()
    serializer_class = serializers.ComplexNewsSerializer
    http_method_names = ('put', 'post', 'delete')
    permission_classes = [IsComplexOwner]

    def create(self, request, *args, **kwargs):
        return create_related_object(self, request, *args, **kwargs)


@extend_schema(tags=["apartments"])
class ApartmentViewSet(PsqMixin, viewsets.ModelViewSet):
    queryset = models.Apartment.objects.filter(is_moderated=True)\
        .prefetch_related('apartment_images', 'apartment_ad',).\
        select_related('owner')
    serializer_class = serializers.ApartmentRestrictedSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = AdvertisementFilter
    psq_rules = {
        ('list', 'add_flat_to_favourite'): [
            Rule([IsAuthenticated]),
        ],
        'create': [
            Rule([IsAuthenticated])
        ],
        ('update', 'partial_update', 'destroy',
         "flat-list-for-user", "flat-for-user"): [
            Rule([IsAdminUser]),
            Rule([IsApartmentOwner])
        ],
    }

    def get_queryset(self):
        if self.action == 'update' or self.action == 'destroy' or self.action == "partial_update":
            return models.Apartment.objects.all()\
                .prefetch_related('apartment_images', 'apartment_ad',).\
                select_related('owner')
        return self.queryset

    def list(self, request, *args, **kwargs):
        serializer = serializers.MyApartmentsSerializer(self.queryset,
                                                        many=True)
        return Response(serializer.data)

    @extend_schema(request=serializers.ApartmentSerializer,
                   responses={201: OpenApiResponse(
                       response=serializers.ApartmentSerializer)})
    def create(self, request, *args, **kwargs):
        serializer = serializers.ApartmentSerializer(data=request.data,
                                           context={'owner': self.request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        apartment_obj = self.get_object()
        if all([request.user != apartment_obj.owner,
                not request.user.is_staff]):
            apartment_obj.is_viewed.add(request.user)
            serializer = serializers.ApartmentDetailSerializer(apartment_obj)
        else:
            serializer = serializers.ApartmentOwnerSerializer(apartment_obj)
        return Response(serializer.data)

    @extend_schema(request=serializers.ApartmentSerializer,
                   responses={200: OpenApiResponse(
                       response=serializers.ApartmentSerializer)}
                   )
    def update(self, request, *args, **kwargs):
        apartment = self.get_object()
        if apartment and apartment.owner == request.user:
            serializer = serializers.ApartmentSerializer(apartment, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK )
        return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(tags=["favourites"],
                   request=serializers.serializers.Serializer,)
    @action(detail=True, name='add_flat_to_favourite', methods=["put"])
    def add_flat_to_favourite(self, request, *args, **kwargs):
        apartment = self.get_object()
        if apartment in request.user.favourite_apartment.all():
            request.user.favourite_apartment.remove(apartment)
            return Response({'message':"Удалено"})
        request.user.favourite_apartment.add(apartment)
        return Response({"message": "Добавлено"})

    @extend_schema(tags=["favourites"],
                   request=serializers.serializers.Serializer,
                   responses={200: OpenApiResponse(
                       response=serializers.ApartmentRestrictedSerializer)}
                   )
    @action(detail=False, name='favourites_apartments', methods=["get"])
    def favourites_apartment(self, request, *args, **kwargs):
        apartments = request.user.favourite_apartment.all()
        serializer = serializers.ApartmentRestrictedSerializer(
            apartments, many=True
        )
        return Response(serializer.data)

    @extend_schema(responses={200: OpenApiResponse(
        response=serializers.MyApartmentsSerializer)})
    @action(detail=False, name="flat-list-for-user", methods=["get"],
            url_path="my-apartment-list")
    def flats_list(self, request):
        apartments = models.Apartment.objects.filter(owner=request.user)
        serializer = serializers.MyApartmentsSerializer(
            apartments, many=True
        )
        return Response(serializer.data)


@extend_schema(tags=["booking"])
class ApartmentBookingViewSet(mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    serializer_class = serializers.ApartmentBookingSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ApartmentFilter
    http_method_names = ("get", "put")
    permission_classes = [IsAuthenticated]
    queryset = models.Apartment.objects.filter(is_moderated=True)

    def get_queryset(self):
        complex_id = self.request.query_params.get('complex_id')
        if complex_id:
            queryset = models.Apartment.objects.filter(is_moderated=True,
                                                       complex_id=complex_id)
            return queryset
        return models.Apartment.objects.filter(is_moderated=True)

    @extend_schema(tags=["booking"], parameters=[
                       OpenApiParameter(
                           name='complex_id',
                           description='Required query parameter '
                                       '(id residential complex) to get a list'
                                       ' of apartments in '
                                       'this residential complex',
                           required=True, type=int)])
    def list(self, request, *args, **kwargs):
        return super(ApartmentBookingViewSet, self).list(request,
                                                         *args,
                                                         **kwargs)


@extend_schema(tags=["moderation"])
class ApartmentModerationViewSet(viewsets.ModelViewSet):
    queryset = models.Apartment.objects.filter(
        ~Q(moderation_decide='Подтверждено')
    ).prefetch_related('apartment_images')
    serializer_class = serializers.ApartmentModerationList
    http_method_names = ("get", "put", "delete")
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(is_moderated=False)
        serializer = self.serializer_class(
            queryset, many=True
        )
        return Response(serializer.data)

    @extend_schema(request=serializers.ApartmentModerationObject)
    def retrieve(self, request, *args, **kwargs):
        apartment_obj = self.get_object()
        serializer = serializers.ApartmentModerationObject(
            apartment_obj
        )
        return Response(serializer.data)

    @extend_schema(request=serializers.ApartmentModerationObject)
    def update(self, request, *args, **kwargs):
        apartment_obj = self.get_object()
        serializer = serializers.ApartmentModerationObject(
            apartment_obj, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@extend_schema(tags=["advertisement"])
class AdvertisementViewSer(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = models.Advertisement.objects.all()
    serializer_class = serializers.AdvertisementSerializer
    http_method_names = ["put"]
    lookup_field = 'apartment'
    permission_classes = [IsApartmentOwner]


@extend_schema(tags=["complaint"])
class ComplaintViewSet(PsqMixin, viewsets.ModelViewSet):
    queryset = models.Complaint.objects.all()
    serializer_class = serializers.ComplaintSerializer
    http_method_names = ["get", "post", "put", "delete"]

    psq_rules = {
        ('list', 'delete', 'retrieve', 'destroy'): [
            Rule([IsAdminUser]),
        ],
        'create': [
            Rule([IsAuthenticated], )
        ],
    }

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
