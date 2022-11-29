from dj_rest_auth.registration.views import VerifyEmailView
from drf_psq import Rule, PsqMixin

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from users import models, serializers


@extend_schema(tags=["cabinet"])
class UserViewSet(PsqMixin, viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.CustomUser.objects.all()
    psq_rules = {
        ('list', 'add_to_blacklist', 'blacklist', 'destroy'): [
            Rule([IsAdminUser]),
        ],
        ('update', 'partial_update'): [
            Rule([IsAuthenticated],)
        ],
    }

    @action(detail=True, methods=["put"], name="subscription_continue")
    def subscription_continue(self, request, *args, **kwargs):
        subscription = get_object_or_404(models.Subscription,
                                         user=request.user)
        serializer = serializers.SubscriptionSerializer(
            subscription,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = serializers.UsersListSerializer(
            queryset, many=True
        )
        return Response({'data': serializer.data,
                         'count': queryset.count()})

    @action(detail=False, methods=["get"], name="blacklist")
    def blacklist(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(is_blacklisted=True)
        serializer = serializers.UsersListSerializer(
            queryset, many=True
        )
        return Response({'data': serializer.data,
                         'count': queryset.count()})

    @extend_schema(request=serializers.serializers.Serializer)
    @action(detail=True, methods=["put"], name="add_to_blacklist")
    def add_to_blacklist(self, request, *args, **kwargs):
        user = get_object_or_404(models.CustomUser, pk=kwargs.get("pk"))
        if not user.is_blacklisted:
            user.is_blacklisted = True
            user.save()
            return Response('Пользователь добавлен в  черный список')
        user.is_blacklisted = False
        user.save()
        return Response('Пользователь уделен из черного списка')

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@extend_schema(tags=["notary"])
class NotaryViewSet(PsqMixin, viewsets.ModelViewSet):
    queryset = models.Notary.objects.all()
    serializer_class = serializers.NotarySerializer

    psq_rules = {
        ('create', 'update', 'partial_update', 'destroy'): [
            Rule([IsAdminUser]),
        ],
    }


@extend_schema(tags=["messages"])
class MessagesViewSet(viewsets.GenericViewSet):
    http_method_names = ("get", "post", "delete")
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageListSerializer
    lookup_field = "recipient_id"

    def retrieve(self, request, *args, **kwargs):
        recipient = get_object_or_404(models.CustomUser,
                                      pk=kwargs.get("recipient_id"))
        queryset_outbox = self.queryset.filter(sender=request.user,
                                               recipient=recipient)
        queryset_inbox = self.queryset.filter(recipient=request.user,
                                              sender=recipient)
        total_qs = queryset_inbox | queryset_outbox
        serializer = serializers.MessageListSerializer(total_qs, many=True)
        return Response(serializer.data)

    @extend_schema(request=serializers.MessageSerializer)
    @action(detail=True,
            name="send",
            methods=("get",),
            url_path="feedback_detail")
    def retrieve_feedback(self, request, *args, **kwargs):
        queryset = self.queryset.filter(is_feedback=True)
        recipient = get_object_or_404(models.CustomUser,
                                      pk=kwargs.get("recipient_id"))
        queryset_outbox = queryset.filter(sender=request.user,
                                          recipient=recipient)
        queryset_inbox = queryset.filter(recipient=request.user,
                                         sender=recipient)
        total_qs = queryset_inbox | queryset_outbox
        serializer = serializers.MessageListSerializer(total_qs, many=True)
        return Response(serializer.data)

    @extend_schema(request=serializers.MessageSerializer)
    @action(detail=True, name="send", methods=("post",), url_path="send")
    def send_message(self, request, *args, **kwargs):
        recipient = get_object_or_404(models.CustomUser,
                                      pk=kwargs.get(self.lookup_field))
        serializer = serializers.MessageSerializer(data=request.data,
                                                   context={
                                                       'sender': request.user,
                                                       'recipient': recipient,
                                                   })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("success")

    @extend_schema(request=serializers.MessageSerializer)
    @action(detail=True, name="send", methods=("post",),
            url_path="send_feedback")
    def send_feedback(self, request, *args, **kwargs):
        recipient = get_object_or_404(models.CustomUser,
                                      pk=kwargs.get(self.lookup_field))
        serializer = serializers.MessageSerializer(data=request.data,
                                                   context={
                                                       'sender': request.user,
                                                       'recipient': recipient,
                                                       'is_feedback': True
                                                   })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("success")


class VerifyEmailViewCustom(VerifyEmailView):

    def get(self, *args, **kwargs):
        key = self.request.path.split('/')[-2]
        serializer = self.get_serializer(data={'key': key})
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'detail': _('ok')}, status=status.HTTP_200_OK)


@extend_schema(tags=["filters"])
class FilterViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FilterSerializer

    def get_queryset(self):
        queryset = models.Filter.objects.filter(user=self.request.user)
        return queryset


@extend_schema(tags=["many_functional_center"])
class ManyFunctionalCenterViewSet(PsqMixin, viewsets.ModelViewSet):
    serializer_class = serializers.ManyFunctionalCenterSerializer
    queryset = models.ManyFunctionalCenter.objects.all()

    psq_rules = {
        ('list', 'retrieve'): [
            Rule([IsAdminUser]),
            Rule([IsAuthenticated]),
        ],
        ('create', 'update', 'partial_update', 'destroy'): [
            Rule([IsAdminUser], )
        ],
    }
