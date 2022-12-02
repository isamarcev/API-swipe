from allauth.account.models import EmailAddress
from django.core.management import BaseCommand
from faker import Faker

from APISwipe import settings
from users.models import CustomUser


fake = Faker('ru_RU')


class Command(BaseCommand):
    help = 'Create developers'

    def handle(self, *args, **kwargs):
        if not settings.DEBUG and not CustomUser.objects.filter(is_staff=False, is_developer=True).exists():
            for i in range(2):
                user = CustomUser.objects.create(
                    is_developer=True,
                    first_name=fake.first_name_male(),
                    last_name=fake.last_name_male(),
                    email=fake.email(),
                    phone=f'+38 066 666 66 {i}6'
                )
                user.set_password('qwerty40req')
                user.save()
                EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
            self.stdout.write("Developers successfully created")