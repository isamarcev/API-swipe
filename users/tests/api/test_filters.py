import json

import pytest
from django.urls import reverse
from model_bakery import baker
from users.models import Filter

pytestmark = pytest.mark.django_db


class TestNotary:
    endpoint = "/users/filters/"

    def create(self, client, user):
        client.force_authenticate(user=user)
        filter = baker.prepare(Filter, user=user)
        json_data = {
            "name": filter.name,
            "apartment_type": "Новострои",
            "status": "ready",
            "district": filter.district,
            "microdistrict": filter.microdistrict,
            "rooms": filter.rooms,
            "price_low": 1100,
            "price_high": 1200,
            "area_low": 1300,
            "area_high": 1400,
            "purpose": "flat",
            "payment_options": "onlycash",
            "user": filter.user.id
        }
        response = client.post(self.endpoint, data=json_data,
                               format="json")
        assert response.status_code == 201

    def update(self, client, user, user_lier):
        client.force_authenticate(user=user)
        old_filter = baker.make(Filter, user=user)
        json_data = {
            "name": "Новостройка",
            "apartment_type": "Новострои",
            "status": "ready",
            "district": "",
            "microdistrict": "",
            "rooms": "",
            "price_low": 1100,
            "price_high": 1200,
            "area_low": 1300,
            "area_high": 1400,
            "purpose": "flat",
            "payment_options": "onlycash",
            "user": user.id
        }
        flag = reverse("filter_viewset-detail", kwargs={"pk": old_filter.id})
        response = client.put(flag, data=json_data,
                              format="multipart")
        client.force_authenticate(user=user_lier)

        response_lies = client.put(flag, data=json_data, format="multipart")

        assert response.status_code == 200
        assert response_lies.status_code == 404
        Filter.objects.all().delete()

    def test_user(self, client, user_default, user_is_staff):
        self.create(client, user_default)
        self.update(client, user_default, user_is_staff)



