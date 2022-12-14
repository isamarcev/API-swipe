# Generated by Django 4.1.3 on 2022-11-24 22:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0023_alter_advertisement_apartment'),
        ('users', '0013_alter_contact_email_alter_contact_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='favourite_apartment',
            field=models.ManyToManyField(to='content.apartment'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='favourite_complex',
            field=models.ManyToManyField(to='content.complex'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 25, 0, 37, 52, 724035), null=True),
        ),
    ]
