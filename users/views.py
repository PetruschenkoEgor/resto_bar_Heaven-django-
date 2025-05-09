from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, UpdateView

from config.settings import EMAIL_HOST_USER
from resto.models import Reservation
from users.forms import UserRegisterForm
from users.models import User


class UserCreateView(CreateView):
    """Регистрация пользователя"""

    model = User
    form_class = UserRegisterForm
    template_name = "user-form.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        """При успешной регистрации, отправляется письмо на почту."""
        user = form.save()
        send_mail(
            subject=f"{user.name}, Вы успешно зарегистрировались",
            message=f"{user.name}, приветствуем Вас в нашем ресторане HEAVEN! Вы успешно зарегистрировались "
                    f"и можете войти в свой личный кабинет!",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    """Редактирование пользователя."""

    model = User
    form_class = UserRegisterForm
    template_name = "user-form.html"
    success_url = reverse_lazy("users:personal-account")


class PersonalAccountDetailView(DetailView):
    """Личный кабинет."""

    model = User
    template_name = "personal_account.html"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        """Передача в контекст информации о бронированиях пользователя."""

        context = super().get_context_data(**kwargs)
        context["reservations"] = Reservation.objects.filter(user=self.kwargs.get("pk")).order_by("-start_datetime")
        context["now"] = timezone.now()
        return context
