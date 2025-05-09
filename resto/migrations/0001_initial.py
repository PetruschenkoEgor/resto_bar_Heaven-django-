# Generated by Django 5.1.7 on 2025-03-27 05:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Table",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "number_table",
                    models.PositiveIntegerField(
                        help_text="Введите номер столика", unique=True, verbose_name="Номер столика"
                    ),
                ),
                (
                    "capacity",
                    models.PositiveIntegerField(
                        help_text="Введите вместимость столика", verbose_name="Вместимость столика"
                    ),
                ),
            ],
            options={
                "verbose_name": "Столик",
                "verbose_name_plural": "Столики",
            },
        ),
        migrations.CreateModel(
            name="Reservation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "reservation_date",
                    models.DateField(help_text="Введите дату бронирования", verbose_name="Дата бронирования"),
                ),
                (
                    "reservation_time",
                    models.TimeField(help_text="Введите время бронирования", verbose_name="Время бронирования"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания бронирования")),
                (
                    "user",
                    models.ForeignKey(
                        help_text="Введите гостя",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Гость",
                    ),
                ),
                (
                    "table",
                    models.ForeignKey(
                        help_text="Введите номер столика",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="resto.table",
                        verbose_name="Номер столика",
                    ),
                ),
            ],
            options={
                "verbose_name": "Бронирование",
                "verbose_name_plural": "Бронирования",
                "constraints": [
                    models.UniqueConstraint(
                        fields=("table", "reservation_date", "reservation_time"), name="unique_reservation"
                    )
                ],
            },
        ),
    ]
