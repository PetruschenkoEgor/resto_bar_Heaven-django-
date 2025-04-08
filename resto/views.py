import json
from datetime import timedelta, datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, DeleteView, FormView, DetailView

from config import settings
from resto.forms import FeedbackForm, ReservationForm, MenuForm
from resto.models import Table, Reservation, Feedback, Menu, Poster
from users.models import User


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


class MenuListView(ListView):
    """ Страница меню. """

    model = Menu
    template_name = 'menu.html'
    context_object_name = 'menus'


class PosterListView(ListView):
    """ Страница афиши. """

    model = Poster
    template_name = 'poster.html'
    context_object_name = 'posters'


class AboutUsTemplateView(TemplateView):
    """ Страница о нас. """

    template_name = 'about.html'


# class TableCreateView(CreateView):
#     """ Создание столика """
#
#     model = Table
#     template_name = 'add_table.html'
#     success_url = reverse_lazy('resto:tables')


class TableSelectionTemplateView(LoginRequiredMixin, TemplateView):
    """ Просмотр столиков. """

    template_name = 'reservation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tables'] = Table.objects.all()
        return context


class ReservationCreateView(LoginRequiredMixin, CreateView):
    """ Бронирование столика. """

    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_form.html'
    success_url = reverse_lazy('resto:reservation-confirm')

    def get_context_data(self, **kwargs):
        """ Передача столика в контекст. """

        context = super().get_context_data(**kwargs)
        context['table'] = Table.objects.get(pk=self.kwargs.get('pk'))
        return context

    def get_initial(self):
        """ Заполняет форму, имеющимися данными. """

        initial = super().get_initial()
        initial['table'] = self.kwargs.get('pk')
        return initial

    def form_valid(self, form):
        """ Добавляет текущего пользователя в запись бронирования и отправляет письмо. """

        reservation = form.save(commit=False)
        reservation.user = self.request.user
        reservation.save()

        subject = f'Подтверждение бронирования столика №{reservation.table.number_table}'
        message = f'''
                            Здравствуйте!

                            Спасибо за бронирование столика в нашем ресторане HEAVEN.

                            Информация о Вашем бронировании:
                            - Стол №{reservation.table.number_table}
                            - Дата и время бронирования: {reservation.start_datetime.time()} - {reservation.end_datetime.time()} {reservation.start_datetime.date()}
                            - Имя гостя: {reservation.customer_name}
                            - Количество гостей: {reservation.quantity_customers}
                            - Телефон: {reservation.phone_number}

                            Адрес: г.Москва, ул.Пресненская Набережная, 2
                            Телефон: +7 (777) 777-77-77
                            Время работы: пн-вс 10:00-00:00

                            Будем рады приветствовать Вас в нашем ресторане!

                            С уважением,
                            Команда HEAVEN
                            '''
        sender = settings.EMAIL_HOST_USER
        recipient = reservation.user.email
        send_mail(subject, message, sender, [recipient])

        messages.success(self.request,
                         'Ваше бронирование успешно создано! На вашу почту отправлено подтверждающее письмо.')

        return super().form_valid(form)


class ConfirmReservationView(LoginRequiredMixin, FormView):
    """ Подтверждение бронирования. """

    form_class = ReservationForm
    template_name = 'reservation-confirm.html'
    success_url = reverse_lazy('resto:home')

    def form_valid(self, form):
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        """ Передаем текущего пользователя в шаблон. """

        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user

        return context


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирование бронирования. """

    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_form.html'
    success_url = reverse_lazy('users:personal-account')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    """ Удаление бронирования. """

    model = Reservation
    template_name = 'reservation_confirm_delete.html'
    context_object_name = 'reservation'
    success_url = reverse_lazy('users:personal-account')

    def get_context_data(self, **kwargs):
        """ Передача в контекст текущего пользователя. """

        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['now'] = timezone.now()
        return context

    def get_success_url(self):
        """ Перенаправление на личный кабинет. """

        return reverse_lazy('users:personal-account', kwargs={'pk': self.object.user.pk})


class FreeTablesView(LoginRequiredMixin, View):
    """ Свободные столики. """

    def post(self, request):
        data = json.loads(request.body)
        selected_date = data.get('date')
        selected_time = data.get('time')

        # Преобразование строки в объекты datetime
        try:
            selected_datetime = datetime.strptime(f"{selected_date} {selected_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            return JsonResponse({"error": "Некорректный формат даты или времени"}, status=400)

        # Фильтрация доступных столиков
        available_tables = []
        for table in Table.objects.all():
            if table.is_available(selected_datetime, selected_datetime):
                available_tables.append({
                    'id': table.id,
                    'name': table.number_table,
                    'capacity': table.capacity,
                    'image': table.image.url if table.image else None
                })

        return JsonResponse({'tables': available_tables}, safe=False)
