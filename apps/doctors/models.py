from django.db import models
from apps.accounts.models import User


class Specialization(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile', null=True, blank=True)
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True, verbose_name='Специализация')
    photo = models.URLField(blank=True, verbose_name='Фото', default='https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=400')
    experience_years = models.IntegerField(default=0, verbose_name='Опыт (лет)')
    education = models.TextField(blank=True, verbose_name='Образование')
    bio = models.TextField(blank=True, verbose_name='О враче')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0, verbose_name='Рейтинг')
    created_at = models.DateTimeField(auto_now_add=True)

    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'.strip()

    def short_name(self):
        parts = [self.last_name]
        if self.first_name:
            parts.append(self.first_name[0] + '.')
        if self.middle_name:
            parts.append(self.middle_name[0] + '.')
        return ' '.join(parts)

    def appointments_count(self):
        return self.appointments.count()

    def __str__(self):
        return self.full_name()

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'
        ordering = ['last_name', 'first_name']


class Schedule(models.Model):
    DAYS = [(0,'Пн'),(1,'Вт'),(2,'Ср'),(3,'Чт'),(4,'Пт'),(5,'Сб'),(6,'Вс')]
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedule', verbose_name='Врач')
    day_of_week = models.IntegerField(choices=DAYS, verbose_name='День недели')
    start_time = models.TimeField(verbose_name='Начало')
    end_time = models.TimeField(verbose_name='Конец')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.doctor.short_name()} — {self.get_day_of_week_display()} {self.start_time}–{self.end_time}'

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'
        ordering = ['day_of_week', 'start_time']
