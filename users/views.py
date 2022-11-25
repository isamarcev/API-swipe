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

from users import models, serializers
from content.permissions import IsComplexOwner, IsApartmentOwner
from users.permissions import IsDeveloperUser
from content.services.service_serializer import create_related_object


@extend_schema(tags=["cabinet"])
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.CustomUser.objects.all()
    
    @action(detail=True, methods=["put"], name="subscription_continue")
    def subscription_continue(self, request, *args, **kwargs):
        subscription = get_object_or_404(models.Subscription,
                                         user=request.user)
        serializer = serializers.SubscriptionSerializer(
            subscription,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = serializers.UsersListSerializer(
            queryset, many=True
        )
        return Response({'data': serializer.data,
                         'count': queryset.count()})

    @action(detail=False, methods=["get"], name="blacklist")
    def blacklist(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(is_blacklisted=True)
        serializer = serializers.UsersListSerializer(
            queryset, many=True
        )
        return Response({'data': serializer.data,
                         'count': queryset.count()})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



@extend_schema(tags=["notary"])
class NotaryViewSet(viewsets.ModelViewSet):
    queryset = models.Notary.objects.all()
    serializer_class = serializers.NotarySerializer




