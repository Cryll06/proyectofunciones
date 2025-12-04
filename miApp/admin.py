from django.contrib import admin
from .models import Recurso, Reserva, SolicitudAyuda

# Register your models here.
@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'activo')
    list_filter = ('tipo', 'activo')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('rut_solicitante', 'recurso', 'inicio', 'fin')
    list_filter = ('recurso', 'inicio')

@admin.register(SolicitudAyuda)
class SolicitudAyudaAdmin(admin.ModelAdmin):
    list_display = ('rut', 'motivo', 'fecha_solicitud', 'resuelta')
    list_filter = ('motivo', 'resuelta')
    list_editable = ('resuelta',)