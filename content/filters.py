from django_filters import rest_framework as filters

from .models import Apartment, Advertisement


class AdvertisementFilter(filters.FilterSet):
    price = filters.RangeFilter()
    price_per_square_meter = filters.RangeFilter()
    area = filters.RangeFilter()

    class Meta:
        model = Apartment
        fields = (
            "price", "price_per_square_meter", "area", "rooms", "purpose",
            "condition", "payment_options", "complex__status", "complex__type"
        )


class ApartmentFilter(filters.FilterSet):

    class Meta:
        model = Apartment
        fields = (
            "price", "area", "price_per_square_meter", "rooms", "corpus",
            "section", "is_booked", "complex"
        )
