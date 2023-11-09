# Generated by Django 4.2.6 on 2023-11-09 15:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=200, verbose_name="task name")),
                (
                    "memo",
                    models.CharField(
                        blank=True, default="", max_length=300, verbose_name="task memo"
                    ),
                ),
                (
                    "priority",
                    models.IntegerField(
                        choices=[(0, "HIGH"), (1, "MEDIUM"), (2, "LOW")],
                        default=1,
                        verbose_name="task priority",
                    ),
                ),
                (
                    "due_date",
                    models.DateField(
                        default=datetime.date.today, verbose_name="task due date"
                    ),
                ),
            ],
            options={
                "db_table": "tasks",
            },
        ),
    ]
