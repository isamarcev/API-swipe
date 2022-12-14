# Generated by Django 4.1.3 on 2022-11-29 12:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_alter_subscription_expired_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter',
            name='apartment_type',
            field=models.CharField(blank=True, choices=[('new', 'Новострои'), ('secondary', 'Вторичный рынок'), ('cottage', 'Коттеджы')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='filter',
            name='area_high',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='filter',
            name='area_low',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='filter',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='filter',
            name='payment_options',
            field=models.CharField(blank=True, choices=[('onlycash', 'Только наличные'), ('capital', 'Мат. капитал'), ('mortgage', 'Ипотека'), ('no matter', 'Неважно')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='filter',
            name='price_high',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='filter',
            name='price_low',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='filter',
            name='purpose',
            field=models.CharField(blank=True, choices=[('flat', 'Квартира'), ('commercial', 'Для коммерции'), ('living', 'Жилое помещение')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='filter',
            name='rooms',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 29, 14, 46, 52, 784614), null=True),
        ),
    ]
