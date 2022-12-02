import json

import pytest
from django.urls import reverse
from model_bakery import baker
from users.models import Notary

pytestmark = pytest.mark.django_db


class TestNotary:
    endpoint = "/users/notary/"

    def create_notary(self, client, user):
        notary = baker.prepare(Notary, phone='0448985654')
        client.force_authenticate(user=user)
        json_data = {
            "first_name": notary.first_name,
            "last_name": notary.last_name,
            "email": notary.email,
            "phone": notary.phone,
        }
        response = client.post(self.endpoint, data=json_data,
                               format="multipart")
        if not user.is_staff:
            assert response.status_code == 403
        else:
            assert response.status_code == 201
        Notary.objects.all().delete()

    def update_notary(self, client, user):
        client.force_authenticate(user=user)
        old_notary = baker.make(Notary, phone="0730989898")
        new_notary = baker.prepare(Notary, phone="0730989898")
        json_data = {
            "first_name": new_notary.first_name,
            "last_name": new_notary.last_name,
            "email": new_notary.email,
            "phone": new_notary.phone,
        }
        flag = reverse("notary_viewset-detail", kwargs={"pk": old_notary.id})
        response = client.put(flag, data=json_data,
                               format="multipart")
        if not user.is_staff:
            assert response.status_code == 403
        else:
            assert response.status_code == 200
        Notary.objects.all().delete()

    def list_notary(self, client, user):
        client.force_authenticate(user=user)
        notary_list = baker.make(Notary, _quantity=3, phone="0730989898")
        response = client.get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3
        Notary.objects.all().delete()

    def delete_notary(self, client, user):
        client.force_authenticate(user=user)
        notary = baker.make(Notary, phone="0730989898")
        flag = reverse("notary_viewset-detail", kwargs={"pk": notary.id})
        response = client.delete(flag)

        if user.is_staff:
            assert response.status_code == 204
            assert Notary.objects.all().count() == 0
        else:
            assert response.status_code == 403
            assert Notary.objects.all().count() == 1

    def test_developer(self, client, user_is_developer):
        self.create_notary(client, user_is_developer)
        self.update_notary(client, user_is_developer)
        self.list_notary(client, user_is_developer)
        self.delete_notary(client, user_is_developer)

    def test_user(self, client, user_default):
        self.create_notary(client, user_default)
        self.update_notary(client, user_default)
        self.list_notary(client, user_default)
        self.delete_notary(client, user_default)

    def test_staff(self, client, user_is_staff):
        self.create_notary(client, user_is_staff)
        self.update_notary(client, user_is_staff)
        self.list_notary(client, user_is_staff)
        self.delete_notary(client, user_is_staff)
