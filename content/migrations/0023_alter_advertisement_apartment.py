# Generated by Django 4.1.3 on 2022-11-23 22:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0022_alter_apartment_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='apartment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='apartment_ad', to='content.apartment'),
        ),
    ]
