# Generated by Django 4.1.3 on 2022-12-01 07:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_alter_subscription_expired_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='expired_at',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]
