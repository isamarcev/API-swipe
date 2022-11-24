from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

from content.models import Complex


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
    phone = PhoneNumberField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()


class Notary(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = PhoneNumberField
    email = models.EmailField()


class Subscription(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                related_name='subscription')
    expired_at = models.DateTimeField()
    auto_continue = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)


class Filter(models.Model):
    name = models.CharField(max_length=20)
    apartments = [('new', 'Новострои'), ('secondary', 'Вторичный рынок'),
                  ('cottage', 'Коттеджы')]
    apartment_type = models.CharField(max_length=30, choices=apartments)
    status = models.CharField(max_length=20, choices=[('ready', 'Сдан'),
                                                      ('building', 'Строится')])
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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


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

