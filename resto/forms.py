from django.forms import BooleanField, ModelForm

from resto.models import Reservation


class StyleFormMixin:
    """Стилизация формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"


class ReservationForm(StyleFormMixin, ModelForm):
    """ Форма для бронирования столика.  """

    class Meta:
        """ Модель и поля формы. """

        model = Reservation
        fields = "__all__"
