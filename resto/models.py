from django.db import models

from users.models import User


class Table(models.Model):
    """ Модель столика. """
    number_table = models.PositiveIntegerField(verbose_name='Номер столика', help_text='Введите номер столика', unique=True)
    capacity = models.PositiveIntegerField(verbose_name='Вместимость столика', help_text='Введите вместимость столика')
    image = models.ImageField(upload_to='table_images/', blank=True, null=True, verbose_name='Фото столика')
    is_available = models.BooleanField(default=True, verbose_name='Свободен')

    class Meta:
        verbose_name = 'Столик'
        verbose_name_plural = 'Столики'

    def __str__(self):
        return f'Номер столика: {self.number_table}'

    def is_available(self, start_date, end_date):
        if not start_date or not end_date:
            return False
        # Проверяем, есть ли бронирования, которые пересекаются с выбранным интервалом
        overlapping_reservations = Reservation.objects.filter(
            table=self,
            start_datetime__lt=end_date,  # Начало бронирования раньше конца выбранного интервала
            end_datetime__gt=start_date  # Окончание бронирования позже начала выбранного интервала
        )
        return not overlapping_reservations.exists()


class Reservation(models.Model):
    """ Модель бронирования. """
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name='Номер столика')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Гость', blank=True, null=True)
    start_datetime = models.DateTimeField(verbose_name='Время и дата начала бронирования', blank=True, null=True)
    end_datetime = models.DateTimeField(verbose_name='Время и дата окончания бронирования', blank=True, null=True)
    customer_name = models.CharField(max_length=255, verbose_name='Имя гостя', blank=True, null=True)
    quantity_customers = models.PositiveIntegerField(verbose_name='Количество гостей', blank=True, null=True)
    phone_number = models.CharField(max_length=255, verbose_name='Номер телефона', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания бронирования')

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f'Столик {self.table} забронирован на {self.start_datetime}'


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


class Menu(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название', blank=True, null=True)
    image = models.ImageField(upload_to='menu_images', verbose_name='Фото меню', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.title


class Poster(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название', blank=True, null=True)
    image = models.ImageField(upload_to='poster_images', verbose_name='Фото афиши', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Афиша'
        verbose_name_plural = 'Афиша'

    def __str__(self):
        return self.title
