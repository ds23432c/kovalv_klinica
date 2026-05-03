from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.patients_list, name='list'),
    path('<int:pk>/', views.patient_detail, name='detail'),
    path('new/', views.patient_create, name='create'),
    path('<int:pk>/edit/', views.patient_edit, name='edit'),
    path('<int:patient_pk>/record/add/', views.add_medical_record, name='add_record'),
]
