from django.contrib import admin

from resto.models import Reservation, Feedback, Table, Menu, Poster


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "table", "start_datetime", "end_datetime", "customer_name", "phone_number", "user", "created_at")
    list_filter = ("table",)
    search_fields = ("user", "table", "created_at")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "phone", "message")


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("id", "number_table", "capacity")


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description")


@admin.register(Poster)
class PosterAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description")
