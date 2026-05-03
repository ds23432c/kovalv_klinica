from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta, date
from apps.accounts.models import User
from apps.patients.models import Patient
from apps.doctors.models import Doctor, Specialization
from apps.services.models import Service, ServiceCategory
from apps.appointments.models import Appointment


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not (request.user.is_staff or request.user.role == 'admin'):
            return redirect('core:home')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def dashboard(request):
    today = date.today()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    stats = {
        'total_patients': Patient.objects.count(),
        'new_patients_month': Patient.objects.filter(created_at__date__gte=month_ago).count(),
        'total_doctors': Doctor.objects.filter(is_active=True).count(),
        'total_appointments': Appointment.objects.count(),
        'appointments_today': Appointment.objects.filter(date=today).count(),
        'appointments_week': Appointment.objects.filter(date__gte=week_ago).count(),
        'pending_appointments': Appointment.objects.filter(status='pending').count(),
        'completed_appointments': Appointment.objects.filter(status='completed').count(),
        'revenue_month': Appointment.objects.filter(
            date__gte=month_ago, is_paid=True
        ).aggregate(total=Sum('price'))['total'] or 0,
    }

    today_appointments = Appointment.objects.filter(
        date=today
    ).select_related('patient', 'doctor', 'service').order_by('time')

    recent_patients = Patient.objects.order_by('-created_at')[:8]
    top_services = Service.objects.annotate(
        appt_count=Count('appointments')
    ).order_by('-appt_count')[:5]

    return render(request, 'admin_panel/dashboard.html', {
        'stats': stats,
        'today_appointments': today_appointments,
        'recent_patients': recent_patients,
        'top_services': top_services,
        'today': today,
    })


@admin_required
def users_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_panel/users.html', {'users': users})


@admin_required
def toggle_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f'Пользователь {"активирован" if user.is_active else "заблокирован"}')
    return redirect('admin_panel:users')


@admin_required
def appointments_report(request):
    month = request.GET.get('month', str(date.today())[:7])
    appointments = Appointment.objects.filter(
        date__icontains=month
    ).select_related('patient', 'doctor', 'service').order_by('date', 'time')

    stats = {
        'total': appointments.count(),
        'completed': appointments.filter(status='completed').count(),
        'cancelled': appointments.filter(status='cancelled').count(),
        'revenue': appointments.filter(is_paid=True).aggregate(t=Sum('price'))['t'] or 0,
    }
    return render(request, 'admin_panel/report.html', {
        'appointments': appointments,
        'stats': stats,
        'month': month,
    })


@admin_required
def doctors_manage(request):
    doctors = Doctor.objects.select_related('specialization').annotate(
        appt_count=Count('appointments')
    ).order_by('last_name')
    return render(request, 'admin_panel/doctors.html', {'doctors': doctors})


@admin_required
def services_manage(request):
    services = Service.objects.select_related('category').annotate(
        appt_count=Count('appointments')
    ).order_by('category', 'name')
    return render(request, 'admin_panel/services.html', {'services': services})
