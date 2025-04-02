from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView

from resto.forms import ReservationForm, FeedbackForm
from resto.models import Table, Reservation, Feedback


class HomeTemplateView(TemplateView):
    """ Главная страница. """

    template_name = 'home.html'


class FeedbackCreateView(CreateView):
    """ Обратная связь. """

    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback.html'
    success_url = reverse_lazy('resto:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Ваше сообщение успешно отправлено!')
        return response


class AboutUsTemplateView(TemplateView):
    """ Страница о нас. """

    template_name = 'about.html'


class ReservationCreateView(CreateView):
    """ Страница бронирования столика. """

    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation.html'
    success_url = reverse_lazy('resto:home')

    def form_valid(self, form):
        """ При резервировании столика, гостем назначается текущий пользователь. """

        reservation = form.save()
        user = self.request.user
        reservation.user = user
        reservation.save()
        return super().form_valid(form)


# class TableCreateView(CreateView):
#     """ Создание столика """
#
#     model = Table
#     template_name = 'add_table.html'
#     success_url = reverse_lazy('resto:tables')
