import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

from content.models import Complex, Apartment


# Create your models here.


class CustomUser(AbstractUser):
    is_blacklisted = models.BooleanField(_('В черном списке'), default=False)
    is_developer = models.BooleanField(_('Застройщик'), default=False)
    forward_to_agent = models.BooleanField(_('Переключать на агента'),
                                           default=False)
    avatar = models.ImageField(upload_to='users/avatars/',
                               null=True,
                               blank=True)
    notifications = [('Мне', 'Мне'), ('Мне и агенту', 'Мне и агенту'),
                     ('Агенту', 'Агенту'), ('Отключить', 'Отключить')]
    notification_type = models.CharField(max_length=30, choices=notifications,
                                         default=notifications[0][0])
    phone = PhoneNumberField(unique=True, null=False, blank=False)
    email = models.EmailField(_("email address"), blank=True, unique=True)
    username = models.CharField(
        _("username"),max_length=150,)
    favourite_apartment = models.ManyToManyField(Apartment, blank=True)
    favourite_complex = models.ManyToManyField(Complex, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]


class Contact(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                related_name='agent_contacts')
    complex = models.OneToOneField(Complex, on_delete=models.CASCADE,
                                   null=True, blank=True,
                                   related_name='complex_contact')
    contacts = [('Отдел продаж', 'Отдел продаж'), ('Агент', 'Агент')]
    contact_type = models.CharField(max_length=20, choices=contacts)
    phone = PhoneNumberField(null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)


class Notary(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = PhoneNumberField()
    email = models.EmailField()


class Subscription(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                related_name='subscription')
    expired_at = models.DateTimeField(null=True,
                                      default=datetime.datetime.now())
    auto_continue = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)


class Filter(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    apartments = (('Новострои', 'Новострои'),
                  ('Вторичный рынок', 'Вторичный рынок'),
                  ('Коттеджи', 'Коттеджи'))
    apartment_type = models.CharField(max_length=30, choices=apartments,
                                      null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('ready', 'Сдан'),
                                                      ('building', 'Строится')])
    district = models.CharField(max_length=30, null=True, blank=True)
    microdistrict = models.CharField(max_length=30, null=True, blank=True)
    rooms = models.PositiveIntegerField(null=True, blank=True)
    price_low = models.PositiveIntegerField(null=True, blank=True)
    price_high = models.PositiveIntegerField(null=True, blank=True)
    area_low = models.PositiveIntegerField(null=True, blank=True)
    area_high = models.PositiveIntegerField(null=True, blank=True)
    purpose = models.CharField(max_length=30,
                               choices=[('flat', 'Квартира'),
                                        ('commercial', 'Для коммерции'),
                                        ('living', 'Жилое помещение')],
                               null=True, blank=True)
    payments = [('onlycash', 'Только наличные'),
                ('capital', 'Мат. капитал'),
                ('mortgage', 'Ипотека'),
                ('no matter', 'Неважно')]
    payment_options = models.CharField(max_length=30,
                                       choices=payments,
                                       null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Message(models.Model):
    sender = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='outcome_message')
    recipient = models.ForeignKey(CustomUser,
                                  on_delete=models.CASCADE,
                                  related_name='income_message')
    text = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)
    is_feedback = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created', )


class File(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    file = models.FileField(upload_to="files/", null=True)


class ManyFunctionalCenter(models.Model):
    address = models.CharField(max_length=50)
    map_lat = models.DecimalField(decimal_places=8, max_digits=10,
                                  null=True, blank=True)
    map_long = models.DecimalField(decimal_places=8, max_digits=10,
                                   null=True, blank=True)
