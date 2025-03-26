from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")

    name = models.CharField(
        max_length=250,
        verbose_name='Имя',
        help_text='Введите имя',
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=15,
        verbose_name="Номер телефона",
        help_text="Введите номер телефона",
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        help_text="Загрузите свой аватар",
        blank=True,
        null=True,
    )

    # Аутентификация будет по email
    USERNAME_FIELD = "email"
    # Список обязательных для заполнения полей
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
