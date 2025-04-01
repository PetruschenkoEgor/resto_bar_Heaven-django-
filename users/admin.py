from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "name", "phone")
    list_filter = ("name",)
    search_fields = ("email", "name", "phone")
