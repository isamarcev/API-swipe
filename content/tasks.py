from django.core.mail import send_mail
from users.models import Subscription
from .models import Advertisement
from datetime import datetime, timedelta
from APISwipe.celery import app


@app.task
def activate_user_subscription():
    """Renew user's subscription if one is auto-renewal"""
    print("Autorenewal doing")
    subscription = Subscription.objects.filter(auto_continue=True,
                                               expired_at__lt=datetime.now())
    subscription.update(expired_at=datetime.now() + timedelta(days=10),
                        is_active=True)
    print("Auto renewal done")

@app.task
def deactivate_user_subscription():
    """Deactivate if expired at time is low than today"""
    print("Deactivate starting")
    subscription = Subscription.objects.filter(auto_continue=False,
                                               expired_at__lt=datetime.now())
    subscription.update(is_active=False)
    send_mail('SWIPE API',
              'Your subscription has expired',
              None,
              list(subscription.values_list('user__email')),
              fail_silently=False
              )
    print("Deactivate DONE")


@app.task
def deactivate_announcement_advertising():
    """
    Deactivate announcement advertising after the end date
    """
    print('task "deactivate_announcement_advertising" send')
    advertising = Advertisement.objects.filter(is_active=True,
                                               expired_end__lt=datetime.now())
    send_mail('SWIPE',
              'Your advertising has expired',
              None,
              list(advertising.values_list('apartment__owner__email')),
              fail_silently=False
              )
    advertising.update(is_active=False)
    print('task "deactivate_announcement_advertising" complete')