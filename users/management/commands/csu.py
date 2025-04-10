from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Создание суперпользователя"""

    def handle(self, *args, **options):
        email = "admin@example.com"
        if not User.objects.filter(email=email).exists():
            user = User.objects.create(email=email)
            user.set_password("123qwe")
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
