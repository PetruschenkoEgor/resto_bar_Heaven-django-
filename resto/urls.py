from django.urls import path
from resto.apps import RestoConfig
from resto.views import HomeTemplateView, AboutUsTemplateView, FeedbackCreateView, \
    FreeTablesView, TableSelectionTemplateView, ReservationCreateView, ReservationUpdateView, \
    ReservationDeleteView, ConfirmReservationView, MenuListView, PosterListView

app_name = RestoConfig.name

urlpatterns = [
    path('home/', HomeTemplateView.as_view(), name='home'),
    path('about/', AboutUsTemplateView.as_view(), name='about'),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback'),
    path('menu/', MenuListView.as_view(), name='menu'),
    path('posters/', PosterListView.as_view(), name='posters'),
    # path('menu-create/', MenuCreateView.as_view(), name='menu-create'),

    path('table-selection/', TableSelectionTemplateView.as_view(), name='table-selection'),
    path('tables/<int:pk>/reservation/', ReservationCreateView.as_view(), name='reservation'),
    path('free-tables/', FreeTablesView.as_view(), name='free-tables'),
    path('reservation/<int:pk>/edit/', ReservationUpdateView.as_view(), name='reservation-edit'),
    path('reservation/<int:pk>/delete/', ReservationDeleteView.as_view(), name='reservation-delete'),
    path('reservation/confirm/', ConfirmReservationView.as_view(), name='reservation-confirm'),
]
