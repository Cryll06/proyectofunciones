from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('horarios/<int:recurso_id>/', views.ver_horarios, name='ver_horarios'),
    path('confirmar/<int:recurso_id>/', views.confirmar_reserva, name='confirmar_reserva'),
    path('ayuda/', views.ayuda, name='ayuda'),
]