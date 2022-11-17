from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    is_blacklisted = models.BooleanField(null=True,
                                         blank=True)
    is_developer = models.BooleanField(null=True,
                                       blank=True)
    forward_to_agent = models.BooleanField(null=True,
                                           blank=True)
    avatar = models.ImageField(upload_to='users/avatars/',
                               null=True,
                               blank=True)
    notifications = [('me', 'Мне'), ('me and agent', 'Мне и агенту'),
                     ('agent', 'Агенту'), ('turn off', 'Отключить')]
    notification_type = models.CharField(max_length=30, choices=notifications,
                                         default=notifications[0][0])
    phone = models.CharField(max_length=20)


class Contact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    contacts = [('my', 'Мои контакты'), ('agent', 'Контакты агента')]
    contact_type = models.CharField(max_length=20, choices=contacts)
    phone = models.CharField(max_length=20)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()


class Notary(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()


class Subscription(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    expired_at = models.DateTimeField()
    auto_continue = models.BooleanField(null=True, blank=True, default=False)
    is_active = models.BooleanField(null=True, blank=True, default=False)


class Filter(models.Model):
    name = models.CharField(max_length=20)
    apartments = [('new', 'Новострои'), ('secondary', 'Вторичный рынок'),
                  ('cottage', 'Коттеджы')]
    apartment_type = models.CharField(max_length=30, choices=apartments)
    status = models.CharField(max_length=20, choices=[('ready', 'Сдан'),
                                                      'building', 'Строится'])
    district = models.CharField(max_length=30, null=True, blank=True)
    microdistrict = models.CharField(max_length=30, null=True, blank=True)
    rooms = models.PositiveIntegerField()
    price_low = models.PositiveIntegerField()
    price_high = models.PositiveIntegerField()
    area_low = models.PositiveIntegerField()
    area_high = models.PositiveIntegerField()
    purpose = models.CharField(max_length=30,
                               choices=[('flat', 'Квартира'),
                                        ('commercial', 'Для коммерции'),
                                        ('living', 'Жилое помещение')])
    payments = [('onlycash', 'Только наличные'),
                ('capital', 'Мат. капитал'),
                ('mortgage', 'Ипотека'),
                ('no matter', 'Неважно')]
    payment_options = models.CharField(max_length=30,
                                       choices=payments)


class Message(models.Model):
    sender = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='sender')
    recipient = models.ForeignKey(CustomUser,
                                  on_delete=models.CASCADE,
                                  related_name='recipient')
    text = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    is_feedback = models.BooleanField(null=True, blank=True)

