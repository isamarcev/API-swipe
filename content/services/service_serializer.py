from rest_framework.response import Response

from content import models


def update_related_object(serializer, instance, validated_data, field):
    if 'complex_benefits' in validated_data:
        benefits_serializer = serializer.fields[field]
        benefits_instance = getattr(instance, field)
        benefits_data = validated_data.pop(field)
        benefits_serializer.update(benefits_instance, benefits_data)


def create_related_object(serializer, request, *args, **kwargs):
    serializer = serializer.serializer_class(data=request.data,
                                             context={'user': request.user})
    serializer.is_valid(raise_exception=True)
    complex_obj = models.Complex.objects.get(pk=request.data['complex'])
    serializer.save(complex=complex_obj)
    return Response(serializer.data)
