# Generated by Django 4.1.3 on 2022-11-20 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_alter_complexbenefits_complex'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complex',
            name='contact',
        ),
    ]