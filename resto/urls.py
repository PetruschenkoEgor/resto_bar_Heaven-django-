from django.urls import path
from resto.apps import RestoConfig
from resto.views import HomeTemplateView, AboutUsTemplateView, FeedbackCreateView, \
    FreeTablesView, TableSelectionTemplateView, ReservationCreateView, ReservationUpdateView

app_name = RestoConfig.name

urlpatterns = [
    path('home/', HomeTemplateView.as_view(), name='home'),
    path('about/', AboutUsTemplateView.as_view(), name='about'),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback'),

    path('table-selection/', TableSelectionTemplateView.as_view(), name='table-selection'),
    path('tables/<int:pk>/reservation/', ReservationCreateView.as_view(), name='reservation'),
    path('free-tables/', FreeTablesView.as_view(), name='free-tables'),
    path('reservation/<int:pk>/edit/', ReservationUpdateView.as_view(), name='reservation-edit'),
]
