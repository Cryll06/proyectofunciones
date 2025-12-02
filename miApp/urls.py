from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reservar/<int:recurso_id>/', views.crear_reserva, name='crear_reserva'),
]