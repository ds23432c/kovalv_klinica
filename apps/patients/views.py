from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Patient, MedicalRecord
from .forms import PatientForm, MedicalRecordForm


def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role not in ('admin', 'doctor', 'receptionist') and not request.user.is_staff:
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@staff_required
def patients_list(request):
    query = request.GET.get('q', '')
    patients = Patient.objects.all()
    if query:
        patients = patients.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query)
        )
    return render(request, 'patients/list.html', {'patients': patients, 'query': query})


@login_required
@staff_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    records = patient.medical_records.all()
    appointments = patient.appointments.select_related('doctor', 'service').order_by('-date', '-time')
    consents = patient.consents.all()
    return render(request, 'patients/detail.html', {
        'patient': patient,
        'records': records,
        'appointments': appointments,
        'consents': consents,
    })


@login_required
@staff_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'Пациент {patient.full_name()} успешно добавлен!')
            return redirect('patients:detail', pk=patient.pk)
    else:
        form = PatientForm()
    return render(request, 'patients/form.html', {'form': form, 'title': 'Новый пациент'})


@login_required
@staff_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные пациента обновлены!')
            return redirect('patients:detail', pk=pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/form.html', {'form': form, 'title': 'Редактировать пациента', 'patient': patient})


@login_required
@staff_required
def add_medical_record(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.save()
            messages.success(request, 'Медицинская запись добавлена!')
            return redirect('patients:detail', pk=patient_pk)
    else:
        form = MedicalRecordForm()
    return render(request, 'patients/medical_record_form.html', {'form': form, 'patient': patient})
