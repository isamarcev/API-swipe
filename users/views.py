from drf_psq import Rule, PsqMixin

from django.db.models import Max
from django.shortcuts import render

from drf_spectacular.utils import extend_schema

from rest_framework import viewsets, status, mixins
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from users import models, serializers
from content.permissions import IsComplexOwner, IsApartmentOwner
from users.permissions import IsDeveloperUser
from content.services.service_serializer import create_related_object


@extend_schema(tags=["cabinet"])
class UserUpdateView(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.CustomUser.objects.all()
    
    # def get_object(self):
    #     if self.request.user.is_staff:
    #         return super(UserUpdateView, self).get_object()
    #     return self.request.user


    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@extend_schema(tags=["subscription_continue"])
class SubscriptionUpdateView(mixins.UpdateModelMixin,
                             viewsets.GenericViewSet):
    lookup_field = 'user_id'
    serializer_class = serializers.SubscriptionSerializer
    queryset = models.Subscription.objects.all()

    def get_object(self):
        obj = self.queryset.filter(user_id=self.lookup_field)
        print(obj)
        return obj



