# Generated by Django 4.1.3 on 2022-11-20 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_remove_complex_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='price_per_square_meter',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=10),
        ),
    ]
