from django.db import models
from apps.doctors.models import Doctor


class ServiceCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    icon = models.CharField(max_length=10, default='💉', verbose_name='Иконка')
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория услуг'
        verbose_name_plural = 'Категории услуг'
        ordering = ['order']


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, related_name='services', verbose_name='Категория')
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    duration_minutes = models.IntegerField(default=60, verbose_name='Длительность (мин)')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена (руб)')
    price_from = models.BooleanField(default=False, verbose_name='Цена от')
    image_url = models.URLField(blank=True, verbose_name='Изображение')
    doctors = models.ManyToManyField(Doctor, blank=True, related_name='services', verbose_name='Врачи')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    is_popular = models.BooleanField(default=False, verbose_name='Популярная')
    rehabilitation = models.TextField(blank=True, verbose_name='Реабилитация')
    contraindications = models.TextField(blank=True, verbose_name='Противопоказания')
    created_at = models.DateTimeField(auto_now_add=True)

    def price_display(self):
        prefix = 'от ' if self.price_from else ''
        return f'{prefix}{int(self.price):,} ₽'.replace(',', ' ')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['category', 'name']
