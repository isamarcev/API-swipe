from allauth.account.utils import setup_user_email
from django.utils import timezone
from datetime import timedelta
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from users import models
from allauth.account.adapter import DefaultAccountAdapter

from content.serializers import ComplexContactSerializer, UserShortSerializer


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
            username=f'{cleaned_data.get("first_name")} '
                     f'{cleaned_data.get("last_name")}'
        )
        user.set_password(cleaned_data.get('password1'))
        user.save()
        subscription = models.Subscription.objects.create(user=user)
        subscription.save()
        setup_user_email(request, user, [])
        return user


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Subscription
        fields = ("expired_at", "auto_continue", "is_active")
        read_only_fields = ("is_active", 'expired_at', "user")

    def update(self, instance, validated_data):
        if instance.expired_at < timezone.now():
            instance.expired_at = timezone.now() \
                                  + timedelta(minutes=15)
            instance.is_active = True
        return super(SubscriptionSerializer, self).update(instance,
                                                          validated_data)


class UserSerializer(serializers.ModelSerializer):
    agent_contacts = ComplexContactSerializer()
    subscription = SubscriptionSerializer(read_only=True)

    class Meta:
        model = models.CustomUser
        fields = ("first_name", "last_name", "phone", "email",
                  "forward_to_agent", "avatar", "subscription",
                  "agent_contacts",)

    def update(self, instance, validated_data):
        agent_data = validated_data.pop("agent_contacts")
        agent_contact, created = models.Contact.objects.get_or_create(
            user=instance,
            contact_type="Агент"
        )
        agent_contact_serializer = self.fields['agent_contacts']
        agent_contact_serializer.update(instance=agent_contact,
                                        validated_data=agent_data)
        return super(UserSerializer, self).update(instance, validated_data)


class NotarySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Notary
        fields = '__all__'


class UsersListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomUser
        fields = ("first_name", "is_developer", "is_blacklisted",
                  "phone", "email", "avatar",)
        read_only_fields = ("first_name", "is_developer", "is_blacklisted",
                            "phone", "email", "avatar",)


class FileMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.File
        fields = ("file", )


class MessageSerializer(serializers.ModelSerializer):
    file = FileMessageSerializer(allow_null=True, required=False)

    class Meta:
        model = models.Message
        fields = ("text", "file", "created")

    def create(self, validated_data):
        file = validated_data.pop('file')
        message_obj = models.Message.objects.\
            create(**validated_data, **self.context)
        if file:
            models.File.objects.create(**file, message=message_obj)
        return message_obj


class MessageListSerializer(MessageSerializer):
    sender = UserShortSerializer()
    recipient = UserShortSerializer()

    class Meta(MessageSerializer.Meta):
        fields = ("sender", "recipient", "text", "file", "created")
        read_only_fields = ("created", )
