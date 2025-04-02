from django.urls import path
from resto.apps import RestoConfig
from resto.views import HomeTemplateView, AboutUsTemplateView, ReservationCreateView, FeedbackCreateView

app_name = RestoConfig.name

urlpatterns = [
    path('home/', HomeTemplateView.as_view(), name='home'),
    path('about/', AboutUsTemplateView.as_view(), name='about'),
    path('reservation/', ReservationCreateView.as_view(), name='reservation'),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback'),
]
