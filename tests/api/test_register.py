import pytest

from rest_framework.test import APIClient


@pytest.mark.django_db
def test_register_user(client):
    payload = dict(
        first_name="Harry",
        last_name="Potter",
        email="harry@hogwards.com",
        password1="qwerty40req",
        password2="qwerty40req",
        is_developer=False,
        phone="0689897412"
    )
    response = client.post("/users/registration/", data=payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_login_user(user_is_developer, client):
    payload = dict(
        email="harry@hogwards.com",
        password="qwerty40req"
    )
    response = client.post("/users/auth/login/", data=payload)
    assert response.status_code == 200
    assert "access_token" in response.data
    assert "refresh_token" in response.data

