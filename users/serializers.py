from rest_framework import serializers, renderers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from users import models
from allauth.account.adapter import DefaultAccountAdapter

from content.serializers import ComplexContactSerializer


class AuthLoginSerializer(LoginSerializer):
    username = None


class AuthRegisterSerializer(RegisterSerializer):
    phone = PhoneNumberField()
    username = None
    first_name = serializers.CharField(
        max_length=150,
        min_length=2,
        required=True
    )
    last_name = serializers.CharField(
        max_length=150,
        min_length=2,
        required=True
    )

    def get_cleaned_data(self):
        return {
            "phone": self.data.get("phone"),
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", "")
        }

    def save(self, request):
        cleaned_data = self.get_cleaned_data()
        user = models.CustomUser.objects.create(
            email=cleaned_data.get('email'),
            first_name=cleaned_data.get('first_name'),
            last_name=cleaned_data.get('last_name'),
            phone=cleaned_data.get('phone'),
            usernema=f'{cleaned_data.get("first_name")} '
                     f'{cleaned_data.get("last_name")}'
        )
        user.set_password(cleaned_data.get('password1'))
        user.save()
        models.Subscription.objects.create(

        )
        return user


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Subscription
        fields = ("expired_at", "auto_continue", "is_active")


class UserSerializer(serializers.ModelSerializer):
    agent_contacts = ComplexContactSerializer()
    subscription = SubscriptionSerializer()

    class Meta:
        model = models.CustomUser
        fields = ("first_name", "last_name", "phone", "email",
                  "forward_to_agent", "avatar", "subscription",
                  "agent_contacts",)

    # def update(self, instance, validated_data):
