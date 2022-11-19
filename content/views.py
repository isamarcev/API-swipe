from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from content import models, serializers


@extend_schema(tags=["complex"])
class ComplexViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ComplexSerializer

    def list(self, request, *args, **kwargs):
        queryset = models.Complex.objects.filter(owner_id=request.user.id)
        serializer = serializers.ComplexSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = serializers.ComplexSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
