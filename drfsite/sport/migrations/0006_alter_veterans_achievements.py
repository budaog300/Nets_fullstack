# Generated by Django 5.1.6 on 2025-02-28 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0005_alter_clubs_director'),
    ]

    operations = [
        migrations.AlterField(
            model_name='veterans',
            name='achievements',
            field=models.JSONField(blank=True, default=dict, verbose_name='Перечень наград'),
        ),
    ]
