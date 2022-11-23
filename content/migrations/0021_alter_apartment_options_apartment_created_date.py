# Generated by Django 4.1.3 on 2022-11-23 12:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0020_alter_corpus_complex'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apartment',
            options={'ordering': ['-created_date']},
        ),
        migrations.AddField(
            model_name='apartment',
            name='created_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
