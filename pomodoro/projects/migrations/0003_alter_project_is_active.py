# Generated by Django 4.2.6 on 2024-11-17 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="project 활성화 여부"),
        ),
    ]