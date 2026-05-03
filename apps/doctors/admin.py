from django.contrib import admin
from .models import Doctor, Specialization, Schedule

class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'specialization', 'experience_years', 'rating', 'is_active']
    list_filter = ['specialization', 'is_active']
    search_fields = ['first_name', 'last_name']
    inlines = [ScheduleInline]

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name']
