from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('doctor', 'Врач'),
        ('receptionist', 'Регистратор'),
        ('patient', 'Пациент'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    avatar = models.URLField(blank=True, default='https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=200')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.get_full_name() or self.email}'

    def is_admin_role(self):
        return self.role == 'admin' or self.is_staff

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
