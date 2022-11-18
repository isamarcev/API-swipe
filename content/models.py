from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from APISwipe.settings import AUTH_USER_MODEL


class Complex(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    contact = models.ForeignKey(AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='complex_contact')
    name = models.CharField(max_length=50)
    created_date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    address = models.CharField(max_length=100)
    map_lat = models.DecimalField(decimal_places=10, max_digits=10,
                                  null=True, blank=True)
    map_long = models.DecimalField(decimal_places=10, max_digits=10,
                                   null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('ready', 'Сдан'),
                                                      ('building', 'Строится')])
    type = models.CharField(max_length=20, choices=[('panel', 'Панельный'),
                                                    ('brick', 'Кирпичный')])
    klass = models.CharField(max_length=15, choices=[('elit', 'Елитный'),
                                                     ('budget', 'Бюджетный')])
    technology = models.CharField(max_length=50,
                                  choices=[('monolite',
                                            'Монолитный каркас с '
                                            'керамзитным поддоном'),
                                           ('brick', 'Жженый кирпич октябрь')])
    territory = models.CharField(max_length=50,
                                 choices=[('closed', 'Закрытая охраняемая'),
                                          ('open', 'Открытая с доступом')])
    distance_to_sea = models.PositiveIntegerField(null=True, blank=True)
    invoice = models.CharField(max_length=30,
                               choices=[('invoice', 'Платежи'),
                                        ('transaction', 'Актиный платеж')],
                               default='invoice')
    cell_height = models.DecimalField(max_digits=3, decimal_places=1,
                                      default=2.5)
    gas = models.BooleanField(null=True, blank=True)
    electricity = models.CharField(max_length=10,
                                   choices=[('connect', 'Подключено'),
                                            ('disconnect', 'Отключено')],
                                   default='connect')
    heating = models.CharField(max_length=10,
                               choices=[('central', 'Центральное'),
                                        ('auto', 'Автономное')],
                               default='central')
    water_cupply = models.CharField(max_length=10,
                                    choices=[('central', 'Центральное'),
                                             ('auto', 'Автономное')],
                                    default='central')
    sewerage = models.CharField(max_length=10,
                                choices=[('central', 'Центральное'),
                                         ('auto', 'Автономное')],
                                default='central')
    formalization = models.CharField(max_length=20,
                                     choices=[('justice', 'Юстиция'),
                                              ('proxy', 'Доверенность')],
                                     default='justice')
    PAYMENTS = (('onlycash', 'Только наличные'),
                ('capital', 'Мат. капитал'),
                ('mortgage', 'Ипотека'),
                ('no matter', 'Неважно'))
    payment_form = models.CharField(max_length=20, choices=PAYMENTS,
                                    default='onlycash')
    purpose = models.CharField(max_length=30,
                               choices=[('flat', 'Квартира'),
                                        ('commercial', 'Для коммерции'),
                                        ('living', 'Жилое помещение')],
                               default='flat')
    payments_part = models.CharField(max_length=20,
                                     choices=[('all', 'Полная'),
                                              ('part', 'Неполная')],
                                     default='all')



class ComplexSalesDepartment(models.Model):
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = PhoneNumberField
    email = models.EmailField()


class ComplexNews(models.Model):
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE)
    title = models.CharField(max_length=10)
    description = models.CharField(max_length=300)
    created = models.DateField(auto_now_add=True)


class ComplexBenefits(models.Model):
    complex = models.OneToOneField(Complex, on_delete=models.CASCADE)
    parking = models.BooleanField(null=True, blank=True)
    school = models.BooleanField(null=True, blank=True)
    playground = models.BooleanField(null=True, blank=True)
    hospital = models.BooleanField(null=True, blank=True)


class ComplexImage(models.Model):
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f'complexes/{complex.name}/image/')


class ComplexDocument(models.Model):
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    file = models.FileField(upload_to=f'complexes/{complex.name}/document/')


class Corpus(models.Model):
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)


class Section(models.Model):
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    floor_count = models.PositiveIntegerField()


class Floor(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()


class Riser(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()


class Apartment(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE)
    moderation_status = models.CharField(max_length=20,
                                         choices=[
                                             ('price', 'Некорректная цена'),
                                             ('photo', 'Некорректное фото'),
                                             ('description',
                                              'Некорректное описание')
                                         ], null=True, blank=True)
    moderation_decide = models.CharField(max_length=20,
                                         choices=[('confirm', 'Отказано'),
                                                  ('reject', 'Отклонено')])
    is_booked = models.BooleanField(null=True, blank=True)
    number = models.PositiveIntegerField()
    corpus = models.PositiveIntegerField()
    section = models.PositiveIntegerField()
    floor = models.PositiveIntegerField()
    rises = models.PositiveIntegerField()
    description = models.CharField(max_length=500, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    foundation = models.CharField(max_length=200,
                                  choices=[('Фз 2014', 'Фз 2014'),
                                           ('random', 'Случайная')])
    purpose = models.CharField(max_length=20,
                               choices=[('apartment', 'Апартаменты'),
                                        ('cottage', 'Коттедж'),
                                        ])
    rooms = models.PositiveIntegerField()
    plan = models.CharField(max_length=30,
                            choices=[('studio', 'Студия, санузел'),
                                     ('simple', 'Обычная')])
    condition = models.CharField(max_length=30,
                                 choices=[('repairNeeded', 'Требуется ремонт'),
                                          ('living', 'Жилое'),
                                          ('empty', 'Голые стены')])
    area = models.DecimalField(max_digits=2, decimal_places=2)
    kitchenArea = models.DecimalField(max_digits=2, decimal_places=2)
    has_balcony = models.BooleanField(null=True, blank=True)
    heating = models.CharField(max_length=20, choices=[('gas', 'Газовое'),
                                                       ('electro', 'Електро')])
    payments = [('onlycash', 'Только наличные'),
                ('capital', 'Мат. капитал'),
                ('mortgage', 'Ипотека'),
                ('no matter', 'Неважно')]
    payment_options = models.CharField(max_length=30,
                                       choices=payments)
    comission = models.PositiveIntegerField()
    communication_type = models.CharField(max_length=100,
                                          choices=[('callmessage',
                                                    'Звонок + сообщение'),
                                                   ('call',
                                                    'Только звонки'),
                                                   ('message',
                                                    'Сообщение'),
                                                   ])
    price = models.PositiveIntegerField()
    schema = models.ImageField(
        upload_to=f'complexes/{complex.name}/apartment-{number}/schema/')


class ApartmentImage(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=f'apartments/images/', null=True, blank=True)


class Advertisement(models.Model):
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE)
    is_big = models.BooleanField(null=True, blank=True)
    is_up = models.BooleanField(null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True)
    is_turbo = models.BooleanField(null=True, blank=True)
    add_text = models.BooleanField(null=True, blank=True)
    add_color = models.BooleanField(null=True, blank=True)
    text = models.CharField(max_length=20,
                            choices=[
                                ('present', 'Подарок при покупке'),
                                ('bargain', 'Возможен торг'),
                                ('sea', 'Квартира у моря'),
                                ('sleep', 'В спальном районе'),
                                ('price', 'Вам повезло с ценой!'),
                                ('big_family', 'Для большой семьи'),
                                ('family_nest', 'Семейное гнездышко'),
                                ('parking', 'Отдельная парковка'),
                            ])
    color = models.CharField(max_length=20,
                             choices=[('#d13fcf', 'Розовый'),
                                      ('#93cf9b', 'Зеленый')])
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)


class Complaint(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(null=True, blank=True, default=False)

