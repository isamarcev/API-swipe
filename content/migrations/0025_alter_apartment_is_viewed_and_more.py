# Generated by Django 4.1.3 on 2022-11-25 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0024_alter_apartment_moderation_decide'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='is_viewed',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='moderation_decide',
            field=models.CharField(blank=True, choices=[('Подтверждено', 'Подтверждено'), ('Отклонено', 'Отклонено')], max_length=20, null=True),
        ),
    ]