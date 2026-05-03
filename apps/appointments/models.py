from django.db import models
from apps.patients.models import Patient
from apps.doctors.models import Doctor
from apps.services.models import Service


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждён'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён'),
        ('no_show', 'Не явился'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments', verbose_name='Пациент')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments', verbose_name='Врач')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments', verbose_name='Услуга')
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    notes = models.TextField(blank=True, verbose_name='Примечания')
    complaint = models.TextField(blank=True, verbose_name='Жалобы пациента')
    result = models.TextField(blank=True, verbose_name='Результат приёма')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Стоимость')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def status_color(self):
        colors = {
            'pending': 'warning',
            'confirmed': 'primary',
            'completed': 'success',
            'cancelled': 'danger',
            'no_show': 'secondary',
        }
        return colors.get(self.status, 'secondary')

    def __str__(self):
        return f'{self.patient} → {self.doctor.short_name()} {self.date} {self.time}'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-date', '-time']
