import json
from datetime import timedelta, datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView, ListView, UpdateView

from resto.forms import FeedbackForm, ReservationForm
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


# class TableCreateView(CreateView):
#     """ Создание столика """
#
#     model = Table
#     template_name = 'add_table.html'
#     success_url = reverse_lazy('resto:tables')


class TableSelectionTemplateView(TemplateView):
    """ Просмотр столиков. """

    template_name = 'reservation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tables'] = Table.objects.all()
        return context


class ReservationCreateView(CreateView):
    """ Бронирование столика. """

    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_form.html'
    success_url = reverse_lazy('resto:home')

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
        """ Добавляет текущего пользователя в запись бронирования. """

        form.instance.user = self.request.user
        return super().form_valid(form)


class ReservationUpdateView(UpdateView):
    """ Редактирование бронирования. """

    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_form.html'
    success_url = reverse_lazy('users:personal-account')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class FreeTablesView(View):
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
