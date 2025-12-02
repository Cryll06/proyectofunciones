from django.shortcuts import render, redirect, get_object_or_404
from .models import Recurso
from .forms import ReservaForm
from django.contrib import messages

# Create your views here.
def home(request):
    salas = Recurso.objects.filter(activo=True, tipo='SALA')
    pcs = Recurso.objects.filter(activo=True, tipo='PC')
    return render(request, 'home.html', {'salas': salas, 'pcs': pcs})

def crear_reserva(request, recurso_id):
    recurso = get_object_or_404(Recurso, pk=recurso_id)
    
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.recurso = recurso
            reserva.save()
            messages.success(request, 'Reserva realizada con éxito')
            return redirect('home')
    else:
        form = ReservaForm()

    tiempo_fijo = "1 hora" if recurso.tipo == 'PC' else "2 horas"
    
    return render(request, 'form_reserva.html', {
        'form': form, 
        'recurso': recurso,
        'tiempo_fijo': tiempo_fijo
    })