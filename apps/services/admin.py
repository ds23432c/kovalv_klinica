from django.contrib import admin
from .models import Service, ServiceCategory

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'order']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_display', 'duration_minutes', 'is_active', 'is_popular']
    list_filter = ['category', 'is_active', 'is_popular']
    search_fields = ['name']
    filter_horizontal = ['doctors']
