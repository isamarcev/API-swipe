# Generated by Django 4.1.3 on 2022-11-25 11:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_subscription_expired_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 25, 13, 0, 54, 386828), null=True),
        ),
    ]
