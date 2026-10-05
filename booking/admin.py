from django.contrib import admin
from .models import Room, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "capacity", "price_per_night")
    search_fields = ("name",)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "user", "check_in", "check_out", "guests", "created_at")
    list_filter = ("room", "check_in", "check_out")
    search_fields = ("user__username", "room__name")
