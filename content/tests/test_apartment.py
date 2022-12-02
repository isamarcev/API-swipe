from copy import copy

import pytest
from django.urls import reverse
from model_bakery import baker
from content.models import Complex, Apartment
from users.models import Contact
from random import choice
pytestmark = pytest.mark.django_db

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



apartment_data = {
    "number": choice((1, 3, 4, 12)),
    "corpus": choice((1, 3, 4, 12)),
    "section": choice((1, 3, 4, 12)),
    "floor": choice((1, 3, 4, 12)),
    "rises": choice((1, 3, 4, 12)),
    "description": 'choice((1, 3, 4, 12))',
    "address": choice(("Hello world", "DIGI DIGI", "GRIVNA")),
    "foundation": choice(("Фз 2014", "Случайная")),
    "purpose": "Апартаменты",
    "rooms": 4,
    "plan": "Обынчая",
    "condition": "Жилое",
    "heating": "Газовое",
    "payment_options": "Ипотека",
    "communication_type": "Звонок + сообщение",
    "price": choice((12000, 30000, 540000)),
    "comission": choice((120, 300, 540)),
    "area": choice((120, 300, 540)),
    "kitchenArea": choice((12, 30, 54)),
}


class TestApartment:
    endpoint = "/estate/apartment/"

    def create_complex(self, client, user):
        client.force_authenticate(user=user)
        response = client.post("/estate/complex/",
                               data=data, format="json")
        return response.data

    def test_create(self, client, user_default_content, user_is_developer_content):
        complex_obj = self.create_complex(client, user_is_developer_content)
        json_data = apartment_data
        json_data["complex"] = complex_obj.get("id")
        client.force_authenticate(user=user_default_content)
        response = client.post(self.endpoint, data=json_data, format="json")
        assert response.status_code == 201

    def test_update(self, client, user_default_content, user_is_developer_content, user_is_staff_content):
        complex_obj = self.create_complex(client, user_is_developer_content)
        old_data = apartment_data
        old_data["complex"] = complex_obj.get("id")

        client.force_authenticate(user=user_default_content)
        response = client.post(self.endpoint, data=old_data, format="json")
        new_data = copy(old_data)
        new_data["rooms"] = 12
        flag = reverse("apartment-detail",
                       kwargs={'pk': response.data.get('id')})
        response_update = client.put(flag, data=new_data, format="json")

        assert response_update.status_code == 200


