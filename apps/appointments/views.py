from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Appointment
from .forms import AppointmentForm, PublicAppointmentForm, AppointmentStatusForm
from apps.patients.models import Patient
from datetime import date


def book_appointment(request):
    if request.method == 'POST':
        form = PublicAppointmentForm(request.POST)
        if form.is_valid():
            from datetime import date as dt
            dob = dt(2000, 1, 1)
            patient, created = Patient.objects.get_or_create(
                phone=form.cleaned_data['phone'],
                defaults={
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'email': form.cleaned_data.get('email', ''),
                    'date_of_birth': dob,
                    'gender': 'F',
                }
            )
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()
            messages.success(request, f'Запись создана! Мы свяжемся с вами по номеру {patient.phone} для подтверждения.')
            return redirect('core:home')
    else:
        form = PublicAppointmentForm()
    return render(request, 'appointments/book.html', {'form': form})


@login_required
def appointments_list(request):
    if not (request.user.is_staff or request.user.role in ('admin', 'doctor', 'receptionist')):
        return redirect('accounts:login')
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')
    doctor_filter = request.GET.get('doctor', '')
    appointments = Appointment.objects.select_related('patient', 'doctor', 'service').all()
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    if date_filter:
        appointments = appointments.filter(date=date_filter)
    if doctor_filter:
        appointments = appointments.filter(doctor_id=doctor_filter)
    from apps.doctors.models import Doctor
    doctors = Doctor.objects.filter(is_active=True)
    return render(request, 'appointments/list.html', {
        'appointments': appointments,
        'statuses': Appointment.STATUS_CHOICES,
        'doctors': doctors,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'doctor_filter': doctor_filter,
        'today': date.today(),
    })


@login_required
def appointment_detail(request, pk):
    if not (request.user.is_staff or request.user.role in ('admin', 'doctor', 'receptionist')):
        return redirect('accounts:login')
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentStatusForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус записи обновлён!')
            return redirect('appointments:detail', pk=pk)
    else:
        form = AppointmentStatusForm(instance=appointment)
    return render(request, 'appointments/detail.html', {
        'appointment': appointment,
        'form': form,
    })


@login_required
def appointment_create(request):
    if not (request.user.is_staff or request.user.role in ('admin', 'receptionist')):
        return redirect('accounts:login')
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись создана!')
            return redirect('appointments:list')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/form.html', {'form': form, 'title': 'Новая запись'})


@login_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.status = 'cancelled'
    appointment.save()
    messages.info(request, 'Запись отменена.')
    return redirect('appointments:list')
