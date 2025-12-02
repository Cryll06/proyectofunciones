from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['rut_solicitante', 'inicio']
        widgets = {
            'inicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'rut_solicitante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12.345.678-9'}),
        }
        labels = {
            'rut_solicitante': 'Tu RUT',
            'inicio': 'Fecha y Hora de inicio'
        }