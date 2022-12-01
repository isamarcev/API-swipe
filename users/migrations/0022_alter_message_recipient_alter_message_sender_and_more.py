# Generated by Django 4.1.3 on 2022-11-25 12:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_alter_message_options_alter_message_is_feedback_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='income_message', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outcome_message', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 25, 14, 34, 21, 64531), null=True),
        ),
    ]