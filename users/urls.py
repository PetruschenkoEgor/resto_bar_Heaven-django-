from django.urls import path
from users.apps import UsersConfig
from users.views import PersonalAccountDetailView

app_name = UsersConfig.name
urlpatterns = [
    path('personal-account/<int:pk>/', PersonalAccountDetailView.as_view(), name='personal-account'),
]
