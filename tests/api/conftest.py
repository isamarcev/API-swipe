import pytest
from django.contrib.auth import get_user_model
from users.models import CustomUser
from allauth.account.models import EmailAddress
from rest_framework.test import APIClient


User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_is_developer():
    user = CustomUser.objects.create(
        first_name="Harry",
        last_name="Potter",
        email="harry@hogwards.com",
        is_developer=True,
        phone="0689897412"
    )
    user.set_password('qwerty40req')
    user.save()
    EmailAddress.objects.create(
        user=user,
        email=user.email,
        verified=True,
        primary=True
    )
    return user


@pytest.fixture()
def user_is_staff():
    user = CustomUser.objects.create(
        first_name="Ihor",
        last_name="Samartsev",
        email="john@doe.com",
        is_staff=True,
        phone="0689897455"
    )
    user.set_password('qwerty40req')
    user.save()
    EmailAddress.objects.create(
        user=user,
        email=user.email,
        verified=True,
        primary=True
    )
    return user


@pytest.fixture
def user_default():
    user = CustomUser.objects.create(
        first_name="Jimmi",
        last_name="Newton",
        email="england@backward.com",
        phone="0689897413"
    )
    user.set_password('qwerty40req')
    user.save()
    EmailAddress.objects.create(
        user=user,
        email=user.email,
        verified=True,
        primary=True
    )
    return user



