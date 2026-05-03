from django.conf import settings
from apps.patients.models import Patient
from apps.appointments.models import Appointment
from apps.doctors.models import Doctor


def clinic_context(request):
    return {
        'clinic_name': getattr(settings, 'CLINIC_NAME', 'Клиника'),
        'clinic_phone': getattr(settings, 'CLINIC_PHONE', ''),
        'clinic_email': getattr(settings, 'CLINIC_EMAIL', ''),
        'clinic_address': getattr(settings, 'CLINIC_ADDRESS', ''),
        'stat_patients': Patient.objects.count(),
        'stat_doctors': Doctor.objects.filter(is_active=True).count(),
        'stat_appointments': Appointment.objects.count(),
    }
