from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import timedelta

# Create your models here.
class Recurso(models.Model):
    TIPO_RECURSO = (
        ('PC', 'Computadora'),
        ('SALA', 'Sala de Estudio'),
    )
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_RECURSO)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

class Reserva(models.Model):
    rut_validator = RegexValidator(regex=r'^\d{7,8}-[0-9kK]$', message="Formato inválido.")
    rut_solicitante = models.CharField(max_length=12, validators=[rut_validator])
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)
    inicio = models.DateTimeField()
    fin = models.DateTimeField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not getattr(self, 'recurso_id', None) or not self.inicio:
            return
        
        if not self.fin:
            horas = 1 if self.recurso.tipo == 'PC' else 2
            temp_fin = self.inicio + timedelta(hours=horas)
        else:
            temp_fin = self.fin

        reservas_chocan = Reserva.objects.filter(
            recurso=self.recurso,
            inicio__lt=temp_fin,
            fin__gt=self.inicio
        ).exclude(pk=self.pk)

        if reservas_chocan.exists():
            raise ValidationError("Horario ocupado.")
        self.fin = temp_fin

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.rut_solicitante} - {self.recurso}"

class SolicitudAyuda(models.Model):
    MOTIVOS = (
        ('CANCELAR', 'Cancelar una reservación'),
        ('PROBLEMA', 'Informar un problema con sala/PC'),
        ('OTRO', 'Otro asunto'),
    )
    rut_validator = RegexValidator(regex=r'^\d{7,8}-[0-9kK]$', message="Formato inválido.")
    
    rut = models.CharField(max_length=12, validators=[rut_validator])
    motivo = models.CharField(max_length=20, choices=MOTIVOS)
    descripcion = models.TextField()
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    resuelta = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_motivo_display()} - {self.rut}"