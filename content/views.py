from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from content import models, serializers


# Create your views here.
class ComplexViewSet(viewsets.ViewSet):
    serializer_class = serializers.ComplexSerializer

    def list(self, request):
        queryset = models.Complex.objects.filter(owner_id=request.user.id)
        serializer = serializers.ComplexSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = serializers.ComplexSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
