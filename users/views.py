from django.views.generic import DetailView

from users.models import User


class PersonalAccountDetailView(DetailView):
    """ Личный кабинет. """

    model = User
    template_name = "personal_account.html"
    context_object_name = "user"
