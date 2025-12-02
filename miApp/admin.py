from django.contrib import admin
from .models import Recurso, Reserva

# Register your models here.
@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'activo')
    list_filter = ('tipo', 'activo')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('rut_solicitante', 'recurso', 'inicio', 'fin')
    list_filter = ('recurso', 'inicio')