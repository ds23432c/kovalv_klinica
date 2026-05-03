from django import forms
from .models import Patient, MedicalRecord


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'middle_name', 'date_of_birth', 'gender',
                  'phone', 'email', 'address', 'blood_type', 'allergies', 'contraindications', 'notes', 'photo']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'blood_type': forms.Select(attrs={'class': 'form-select'}),
            'allergies': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'contraindications': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['date', 'diagnosis', 'treatment', 'doctor_name', 'notes', 'before_photo', 'after_photo']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'diagnosis': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'treatment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'doctor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'before_photo': forms.URLInput(attrs={'class': 'form-control'}),
            'after_photo': forms.URLInput(attrs={'class': 'form-control'}),
        }
