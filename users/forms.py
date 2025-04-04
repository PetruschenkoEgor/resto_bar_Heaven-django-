from django.contrib.auth.forms import UserCreationForm

from resto.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """ Форма регистрации пользователя. """

    class Meta:
        model = User
        fields = ("email", "name", "phone", "avatar", "password1", "password2")
