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


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'start_datetime', 'end_datetime', 'customer_name', 'quantity_customers', 'phone_number']
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get('table')
        start_datetime = cleaned_data.get('start_datetime')
        end_datetime = cleaned_data.get('end_datetime')
        if not table.is_available(start_datetime, end_datetime):
            raise forms.ValidationError(f"Столик {table} уже забронирован на это время.")
        return cleaned_data


class FeedbackForm(ModelForm):
    """ Форма для обратной связи. """

    class Meta:
        model = Feedback
        fields = ["name", "phone", "message"]
