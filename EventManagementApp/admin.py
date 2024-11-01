from django.contrib import admin
from .models import UserRegistrationModel, Event, Booking

@admin.register(UserRegistrationModel)
class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'gender', 'created_at')
    search_fields = ('full_name', 'email')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'creator', 'max_attendees', 'booked_count')
    search_fields = ('name', 'date', 'location')
    list_filter = ('date',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event')
    search_fields = ('user__username', 'event__name')
