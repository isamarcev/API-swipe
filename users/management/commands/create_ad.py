from random import choice

from django.core.management import BaseCommand

from APISwipe import settings
from users.models import CustomUser
from content.models import Complex, Apartment, Advertisement, ComplexBenefits

class InitData:

    def __init__(self, complex, owner):
        self.apartment_data = {
            "number": choice((1, 3, 4, 12)),
            "corpus": choice((1, 3, 4, 12)),
            "section": choice((1, 3, 4, 12)),
            "floor": choice((1, 3, 4, 12)),
            "rises": choice((1, 3, 4, 12)),
            "description": 'choice((1, 3, 4, 12))',
            "address": choice(("Hello world", "DIGI DIGI", "GRIVNA")),
            "foundation": choice(("Фз 2014", "Случайная")),
            "purpose": "Апартаменты",
            "rooms": 4,
            "plan": "Обынчая",
            "condition": "Жилое",
            "heating": "Газовое",
            "payment_options": "Ипотека",
            "communication_type": "Звонок + сообщение",
            "price": choice((12000, 30000, 540000)),
            "comission": choice((120, 300, 540)),
            "area": choice((120, 300, 540)),
            "kitchenArea": choice((12, 30, 54)),
            "complex": complex,
            "owner": owner,
            "is_moderated": True
        }


data = {
        "name": "NEW COMPLEX",
        "description": "This is very big description ",
        "address": "Nicola Tesla 23",
        "min_price": 23000,
        "price_per_m2": 2220,
        "area_from": 122,
        "area_to": 160,
        "map_lat": None,
        "map_long": None,
        "status": "ready",
        "type": "panel",
        "klass": "elit",
        "technology": "monolite",
        "territory": "closed",
        "distance_to_sea": 2500,
        "invoice": "invoice",
        "cell_height": 2.5,
        "gas": True,
        "electricity": "connect",
        "heating": "central",
        "water_cupply": "central",
        "sewerage": "central",
        "formalization": "justice",
        "payment_form": "onlycash",
        "purpose": "flat",
        "payments_part": "all"
}


class Command(BaseCommand):
    help = 'Create ads for feed and apartments'

    def handle(self, *args, **kwargs):
        if not settings.DEBUG and not Advertisement.objects.all().exists():
            users = CustomUser.objects.filter(is_staff=False,
                                              is_developer=False)
            developers = CustomUser.objects.filter(is_developer=True)
            complex_obj_first = Complex.objects.create(**data, owner=choice(developers))
            data["name"] = "New Complex 2"
            complex_obj_second = Complex.objects.create(**data, owner=choice(developers))
            # apartment_1 = InitData(complex_obj_first).apartment_data
            # apartment_1["complex"] = complex_obj_first
            # apartment_2 = InitData(complex_obj_second).apartment_data
            # apartment_2["complex"] = complex_obj_second
            for i in range(30):
                complex_obj = choice((complex_obj_first, complex_obj_second))
                owner = choice(users)
                apartment_data = InitData(complex_obj, owner).apartment_data
                apartment_obj = Apartment.objects.create(**apartment_data)
                Advertisement.objects.create(apartment=apartment_obj,
                                             created_by=owner)
            self.stdout.write("Ads successfully created")