# Generated by Django 4.1.3 on 2022-11-18 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_alter_complex_cell_height_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complexbenefits',
            name='complex',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='content.complex'),
        ),
    ]
