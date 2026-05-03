from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'service', 'date', 'time', 'status', 'is_paid']
    list_filter = ['status', 'date', 'is_paid', 'doctor']
    search_fields = ['patient__first_name', 'patient__last_name', 'doctor__first_name']
    date_hierarchy = 'date'
    list_editable = ['status', 'is_paid']
