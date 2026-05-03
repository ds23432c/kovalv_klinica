from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.users_list, name='users'),
    path('users/<int:pk>/toggle/', views.toggle_user, name='toggle_user'),
    path('report/', views.appointments_report, name='report'),
    path('doctors/', views.doctors_manage, name='doctors'),
    path('services/', views.services_manage, name='services'),
]
