from django.shortcuts import render, get_object_or_404
from .models import Doctor, Specialization


def doctors_list(request):
    specialization_id = request.GET.get('spec', '')
    doctors = Doctor.objects.filter(is_active=True).select_related('specialization')
    if specialization_id:
        doctors = doctors.filter(specialization_id=specialization_id)
    specializations = Specialization.objects.all()
    return render(request, 'doctors/list.html', {
        'doctors': doctors,
        'specializations': specializations,
        'selected_spec': specialization_id,
    })


def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk, is_active=True)
    schedule = doctor.schedule.filter(is_active=True)
    services = doctor.services.filter(is_active=True)
    return render(request, 'doctors/detail.html', {
        'doctor': doctor,
        'schedule': schedule,
        'services': services,
    })
