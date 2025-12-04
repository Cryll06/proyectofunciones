from django import forms
from .models import Reserva, SolicitudAyuda

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['rut_solicitante']
        widgets = {
            'rut_solicitante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12345678-9'}),
        }
        labels = {'rut_solicitante': 'Tu RUT'}

class SolicitudAyudaForm(forms.ModelForm):
    class Meta:
        model = SolicitudAyuda
        fields = ['rut', 'motivo', 'descripcion']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12345678-9'}),
            'motivo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }