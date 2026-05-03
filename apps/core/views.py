from django.shortcuts import render
from apps.doctors.models import Doctor
from apps.services.models import Service, ServiceCategory
from apps.appointments.models import Appointment


def home(request):
    featured_doctors = Doctor.objects.filter(is_active=True).select_related('specialization')[:6]
    popular_services = Service.objects.filter(is_active=True, is_popular=True)[:6]
    categories = ServiceCategory.objects.all()
    today_appointments = Appointment.objects.filter(
        status__in=['confirmed', 'pending']
    ).select_related('patient', 'doctor').order_by('date', 'time')[:5]
    return render(request, 'core/home.html', {
        'featured_doctors': featured_doctors,
        'popular_services': popular_services,
        'categories': categories,
        'today_appointments': today_appointments,
    })


def contacts(request):
    return render(request, 'core/contacts.html')


def about(request):
    doctors = Doctor.objects.filter(is_active=True).select_related('specialization')
    return render(request, 'core/about.html', {'doctors': doctors})
