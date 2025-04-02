from django.contrib import admin

from resto.models import Reservation, Feedback


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "table", "user", "reservation_date", "reservation_time", "created_at")
    list_filter = ("table", "reservation_date")
    search_fields = ("user", "table", "reservation_date", "reservation_time", "created_at")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "phone", "message")
