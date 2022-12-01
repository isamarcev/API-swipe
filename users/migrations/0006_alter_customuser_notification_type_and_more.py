# Generated by Django 4.1.3 on 2022-11-23 22:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_customuser_forward_to_agent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='notification_type',
            field=models.CharField(choices=[('Мне', 'Мне'), ('Мне и агенту', 'Мне и агенту'), ('Агенту', 'Агенту'), ('Отключить', 'Отключить')], default='Мне', max_length=30),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to=settings.AUTH_USER_MODEL),
        ),
    ]