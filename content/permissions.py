from rest_framework.permissions import IsAuthenticated

from content import models
from users.permissions import IsDeveloperUser


class IsComplexOwner(IsDeveloperUser):

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, models.Complex):
            return bool(request.user.complexes.filter(pk=obj.pk).exists())
        elif isinstance(obj, (models.ComplexNews, models.ComplexImage)):
            return bool(request.user.complexes.
                        filter(pk=obj.complex.pk).exists())
        return False


class IsApartmentOwner(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, models.Apartment):
            print(request.user.apartments.filter(pk=obj.pk).exists(), "BOOL 1")
            return bool(request.user.apartments.filter(pk=obj.pk).exists())
        elif isinstance(obj, models.ApartmentImage):
            print(bool(request.user.apartments.
                        filter(pk=obj.apartment.pk).exists()), "BOOL 2")

            return bool(request.user.apartments.
                        filter(pk=obj.apartment.pk).exists())
        return False
