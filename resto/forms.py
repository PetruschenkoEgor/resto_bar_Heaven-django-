import datetime

from django import forms
from django.forms import BooleanField, ModelForm

from resto.models import Reservation, Feedback


class StyleFormMixin:
    """Стилизация формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"


class ReservationForm(StyleFormMixin, forms.ModelForm):
    """ Форма для бронирования. """

    class Meta:
        model = Reservation
        fields = ['table', 'start_datetime', 'end_datetime', 'customer_name', 'quantity_customers', 'phone_number']
        widgets = {
            'table': forms.Select(attrs={'required': True}),
            # устанавливает календарик на выбор времени и даты и обязательное поле для заполнения
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'required': True}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'required': True}),
        }

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get('table')
        start_datetime = cleaned_data.get('start_datetime')
        end_datetime = cleaned_data.get('end_datetime')

        # время открытия 10:00
        opening_time = datetime.time(hour=10, minute=0)
        if start_datetime.time() < opening_time:
            raise forms.ValidationError("Время начала бронирования должно быть не ранее 10:00 утра.")
        if end_datetime <= start_datetime:
            raise forms.ValidationError("Время окончания бронирования должно быть больше времени начала бронирования.")
        if start_datetime.date() != end_datetime.date():
            raise forms.ValidationError("Даты начала и окончания бронирования должны быть одинаковыми.")
        if not table.is_available(start_datetime, end_datetime):
            raise forms.ValidationError(f"Столик {table} уже забронирован на это время.")
        if not start_datetime or not end_datetime:
            raise forms.ValidationError("Начальная или конечная дата не может быть пустой.")
        return cleaned_data


class FeedbackForm(StyleFormMixin, forms.ModelForm):
    """ Форма для обратной связи. """

    class Meta:
        model = Feedback
        fields = ["name", "phone", "message"]

    def __init__(self, *args, **kwargs):
        """ Отключаем help_text. """

        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None
