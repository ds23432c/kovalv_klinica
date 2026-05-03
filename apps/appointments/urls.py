from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.appointments_list, name='list'),
    path('book/', views.book_appointment, name='book'),
    path('new/', views.appointment_create, name='create'),
    path('<int:pk>/', views.appointment_detail, name='detail'),
    path('<int:pk>/cancel/', views.cancel_appointment, name='cancel'),
]
