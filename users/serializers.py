from rest_framework import serializers

from users import models

from content.serializers import ComplexContactSerializer


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
