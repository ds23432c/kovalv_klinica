from django.db import models
from apps.accounts.models import User


class Patient(models.Model):
    BLOOD_CHOICES = [('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('AB+','AB+'),('AB-','AB-'),('O+','O+'),('O-','O-')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile', null=True, blank=True)
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    gender = models.CharField(max_length=10, choices=[('M','Мужской'),('F','Женский')], verbose_name='Пол')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    address = models.TextField(blank=True, verbose_name='Адрес')
    blood_type = models.CharField(max_length=5, choices=BLOOD_CHOICES, blank=True, verbose_name='Группа крови')
    allergies = models.TextField(blank=True, verbose_name='Аллергии')
    contraindications = models.TextField(blank=True, verbose_name='Противопоказания')
    notes = models.TextField(blank=True, verbose_name='Примечания')
    photo = models.URLField(blank=True, verbose_name='Фото')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'.strip()

    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def __str__(self):
        return self.full_name()

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'
        ordering = ['last_name', 'first_name']


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records', verbose_name='Пациент')
    date = models.DateField(verbose_name='Дата')
    diagnosis = models.TextField(verbose_name='Диагноз / Процедура')
    treatment = models.TextField(verbose_name='Лечение / Описание')
    doctor_name = models.CharField(max_length=200, verbose_name='Врач')
    notes = models.TextField(blank=True, verbose_name='Примечания')
    before_photo = models.URLField(blank=True, verbose_name='Фото до')
    after_photo = models.URLField(blank=True, verbose_name='Фото после')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patient} — {self.date} — {self.diagnosis[:50]}'

    class Meta:
        verbose_name = 'Медицинская запись'
        verbose_name_plural = 'Медицинские записи'
        ordering = ['-date']


class Consent(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consents', verbose_name='Пациент')
    document_type = models.CharField(max_length=200, verbose_name='Тип документа')
    signed_at = models.DateTimeField(verbose_name='Подписано')
    is_signed = models.BooleanField(default=False, verbose_name='Подписано')
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Согласие'
        verbose_name_plural = 'Согласия'
