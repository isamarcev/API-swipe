import pytest
from django.urls import reverse
from model_bakery import baker
from content.models import Complex, ComplexBenefits
from users.models import Contact

data = {
        "name": "NEW COMPLEX",
        "complex_contact": {
            "first_name": "Helen",
            "last_name": "Factory",
            "email": "user1@example.com",
            "phone": "0730233266"
        },
        "complex_benefits": {
            "parking": True,
            "school": True,
            "playground": True,
            "hospital": True
        },
        "description": "This is very big description ",
        "address": "Nicola Tesla 23",
        "min_price": 23000,
        "price_per_m2": 2220,
        "area_from": 122,
        "area_to": 160,
        "map_lat": "",
        "map_long": "",
        "status": "ready",
        "type": "panel",
        "klass": "elit",
        "technology": "monolite",
        "territory": "closed",
        "distance_to_sea": 2500,
        "invoice": "invoice",
        "cell_height": 2.5,
        "gas": True,
        "electricity": "connect",
        "heating": "central",
        "water_cupply": "central",
        "sewerage": "central",
        "formalization": "justice",
        "payment_form": "onlycash",
        "purpose": "flat",
        "payments_part": "all"
}


def checker(user, client):
    client.force_authenticate(user=user)
    response = client.post("/estate/complex/",
                           data=data, format="json")
    if user.is_developer or user.is_staff:
        assert response.status_code == 201
    else:
        assert response.status_code == 403


@pytest.mark.django_db
def test_create_complex_by_staff(user_is_staff_content, client):
    checker(user_is_staff_content, client)


@pytest.mark.django_db
def test_create_complex_by_developer(user_is_developer_content, client):
    checker(user_is_developer_content, client)


@pytest.mark.django_db
def test_create_complex_by_user(user_default_content, client):
    checker(user_default_content, client)


pytestmark = pytest.mark.django_db


class TestUpdateComplex:
    def update_complex(self, client, user):
        client.force_authenticate(user=user)
        response = client.post("/estate/complex/",
                               data=data, format="json")
        flag = reverse("complex-detail", kwargs={'pk': response.data.get('id')})
        data['name'] = "Complex update"
        json_data = data
        response_update = client.put(flag, data=json_data, format="json")
        if user.is_developer and user.id == response_update.data.get('owner'):
            assert response_update.status_code == 200
        elif user.is_staff:
            assert response_update.status_code == 200
        elif not all([user.is_developer, user.is_staff]):
            assert response_update.status_code == 404

    def retrieve(self, client, user, user_is_developer_content=None):
        if user_is_developer_content:
            client.force_authenticate(user=user_is_developer_content)
        else:
            client.force_authenticate(user=user)
        response = client.post("/estate/complex/",
                               data=data, format="json")
        flag = reverse("complex-detail", kwargs={'pk': response.data.get('id')})
        data['name'] = "Complex update"
        if user_is_developer_content:
            client.force_authenticate(user=user)
        response_update = client.get(flag)
        assert response_update.status_code == 200

    def test_developer(self, client, user_is_developer_content):
        self.update_complex(client, user_is_developer_content)
        self.retrieve(client, user_is_developer_content)

    def test_staff(self, client, user_is_staff_content):
        self.update_complex(client, user_is_staff_content)
        self.retrieve(client, user_is_staff_content)

    def test_user(self, client, user_default_content, user_is_developer_content):
        self.update_complex(client, user_default_content)
        self.retrieve(client, user_default_content, user_is_developer_content)




