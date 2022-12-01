import pytest
from model_bakery import baker
from content.models import Complex

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
    # complex_obj = baker.make(Complex, user=user, phone='0730233266')
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
