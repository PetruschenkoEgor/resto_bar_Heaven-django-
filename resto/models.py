from django.db import models

from users.models import User


class Table(models.Model):
    """ Модель столика. """
    number_table = models.PositiveIntegerField(verbose_name='Номер столика', help_text='Введите номер столика', unique=True)
    capacity = models.PositiveIntegerField(verbose_name='Вместимость столика', help_text='Введите вместимость столика')

    class Meta:
        verbose_name = 'Столик'
        verbose_name_plural = 'Столики'

    def __str__(self):
        return f'Номер столика: {self.number_table}'


class Reservation(models.Model):
    """ Модель бронирования. """
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name='Номер столика', help_text='Введите номер столика')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Гость', help_text='Введите гостя', blank=True, null=True)
    reservation_date = models.DateField(verbose_name='Дата бронирования', help_text='Введите дату бронирования')
    reservation_time = models.TimeField(verbose_name='Время бронирования', help_text='Введите время бронирования')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания бронирования')

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        constraints = [
            models.UniqueConstraint(fields=['table', 'reservation_date', 'reservation_time'], name='unique_reservation')
        ]

    def __str__(self):
        return f'Столик {self.table} забронирован на {self.reservation_date}, {self.reservation_time}'


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Гость', help_text='Укажите гостя', blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name='Имя', help_text='Введите имя', blank=True, null=True)
    phone = models.CharField(max_length=30, verbose_name='Номер телефона', help_text='Введите номер телефона')
    message = models.TextField(verbose_name='Сообщение', help_text='Введите сообщение')

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return f'{self.name}: {self.phone}'
