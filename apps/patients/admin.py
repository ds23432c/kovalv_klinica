from django.contrib import admin
from .models import Patient, MedicalRecord, Consent

class MedicalRecordInline(admin.TabularInline):
    model = MedicalRecord
    extra = 0

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'email', 'date_of_birth', 'blood_type', 'created_at']
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    list_filter = ['gender', 'blood_type']
    inlines = [MedicalRecordInline]

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'date', 'diagnosis', 'doctor_name']
    list_filter = ['date']
    search_fields = ['patient__first_name', 'patient__last_name', 'diagnosis']
