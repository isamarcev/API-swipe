# Generated by Django 4.1.3 on 2022-11-24 22:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0023_alter_advertisement_apartment'),
        ('users', '0014_customuser_favourite_apartment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='favourite_apartment',
            field=models.ManyToManyField(blank=True, to='content.apartment'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='favourite_complex',
            field=models.ManyToManyField(blank=True, to='content.complex'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 25, 0, 57, 39, 109872), null=True),
        ),
    ]
