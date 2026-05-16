from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            from datetime import date

            from apps.patients.models import Patient

            user = form.save(commit=False)
            user.phone = form.cleaned_data.get('phone', '')
            user.save()

            # Привязываем профиль пациента к аккаунту, чтобы записи в админке
            # отображались в "Мои записи" после регистрации.
            if user.phone:
                patient, _ = Patient.objects.get_or_create(
                    phone=user.phone,
                    defaults={
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'middle_name': '',
                        'date_of_birth': date(2000, 1, 1),
                        'gender': 'F',
                        'email': user.email or '',
                    },
                )
                if patient.user_id != user.id:
                    patient.user = user
                    patient.save(update_fields=['user'])
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.first_name}! Ваш аккаунт создан.')
            return redirect('core:home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'С возвращением, {user.first_name or user.email}!')
            return redirect(request.GET.get('next', 'core:home'))
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('core:home')


@login_required
def profile_view(request):
    from apps.appointments.models import Appointment
    from apps.patients.models import Patient

    qs = Appointment.objects.filter(patient__user=request.user)

    if not qs.exists() and request.user.phone:
        # Fallback на случай, если Patient.user не заполнен (например, запись была создана до регистрации).
        # phone хранится в отформатированном виде (+7, пробелы, дефисы), поэтому ORM-фильтр по substring может не сработать.
        # Сопоставляем в Python по последним 10 цифрам.
        target_digits = "".join(ch for ch in request.user.phone if ch.isdigit())
        if target_digits:
            last10 = target_digits[-10:] if len(target_digits) >= 10 else target_digits

            matched_patient_ids = []
            for p in Patient.objects.only("id", "phone"):
                p_digits = "".join(ch for ch in (p.phone or "") if ch.isdigit())
                if not p_digits:
                    continue
                p_last10 = p_digits[-10:] if len(p_digits) >= 10 else p_digits
                if p_last10 == last10:
                    matched_patient_ids.append(p.id)

            qs = Appointment.objects.filter(patient_id__in=matched_patient_ids)

    appointments = qs.order_by('-date', '-time')[:10]
    return render(request, 'accounts/profile.html', {
        'appointments': appointments,
    })


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()

            # Обновляем связанные данные Patient, чтобы фильтры профиля работали.
            if user.phone:
                from datetime import date as dt
                from apps.patients.models import Patient

                patient, _ = Patient.objects.get_or_create(
                    user=user,
                    defaults={
                        'phone': user.phone,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'middle_name': '',
                        'date_of_birth': dt(2000, 1, 1),
                        'gender': 'F',
                    },
                )

                # Если существующий Patient был создан до регистрации — проставляем user и телефон.
                patient.phone = user.phone
                patient.first_name = user.first_name
                patient.last_name = user.last_name
                if patient.user_id != user.id:
                    patient.user = user
                patient.save()

            messages.success(request, 'Профиль обновлён!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})
