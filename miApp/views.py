from django.shortcuts import render, redirect, get_object_or_404
from .models import Recurso, Reserva
from .forms import ReservaForm, SolicitudAyudaForm
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta, time

# Create your views here.
def home(request):
    salas = Recurso.objects.filter(activo=True, tipo='SALA')
    pcs = Recurso.objects.filter(activo=True, tipo='PC')
    return render(request, 'home.html', {'salas': salas, 'pcs': pcs})

def ver_horarios(request, recurso_id):
    recurso = get_object_or_404(Recurso, pk=recurso_id)
    
    bloques_diurnos = []
    bloques_vespertinos = []

    if recurso.tipo == 'SALA':
        bloques_diurnos = [(h, 0) for h in range(8, 19, 2)] 
        bloques_vespertinos = [(18, 30), (20, 30)]
        duracion = 2
    else:
        bloques_diurnos = [(h, 0) for h in range(8, 19)]
        bloques_vespertinos = [(18, 30), (19, 30), (20, 30), (21, 30)]
        duracion = 1

    def procesar_bloques(lista_horas):
        resultado = []
        ahora = timezone.now()
        hoy_fecha = ahora.date()

        for h, m in lista_horas:
            inicio_bloque = timezone.make_aware(datetime.combine(hoy_fecha, time(h, m)))
            fin_bloque = inicio_bloque + timedelta(hours=duracion)

            ocupado = Reserva.objects.filter(
                recurso=recurso,
                inicio__lt=fin_bloque,
                fin__gt=inicio_bloque
            ).exists()


            vencido = ahora > inicio_bloque

            resultado.append({
                'inicio': inicio_bloque,
                'hora_texto': f"{inicio_bloque.strftime('%H:%M')} - {fin_bloque.strftime('%H:%M')}",
                'ocupado': ocupado,
                'vencido': vencido
            })
        return resultado

    info_diurno = procesar_bloques(bloques_diurnos)
    info_vesp = procesar_bloques(bloques_vespertinos)

    return render(request, 'ver_horarios.html', {
        'recurso': recurso,
        'bloques_diurnos': info_diurno,
        'bloques_vespertinos': info_vesp
    })

def confirmar_reserva(request, recurso_id):
    recurso = get_object_or_404(Recurso, pk=recurso_id)
    fecha_str = request.GET.get('inicio')
    
    if not fecha_str:
        return redirect('home')

    try:
        fecha_naive = datetime.strptime(fecha_str, "%Y-%m-%d_%H-%M")
        inicio = timezone.make_aware(fecha_naive)
    except ValueError:
        messages.error(request, "Error en la fecha.")
        return redirect('home')
    
    if timezone.now() > inicio:
        messages.error(request, "Ese horario ya ha finalizado.")
        return redirect('ver_horarios', recurso_id=recurso.id)

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            try:
                reserva = form.save(commit=False)
                reserva.recurso = recurso
                reserva.inicio = inicio
                reserva.save()
                messages.success(request, '¡Reserva confirmada!')
                return redirect('home')
            except Exception as e:
                messages.error(request, f"Error: {e}")
        else:
            messages.error(request, "RUT inválido.")
    else:
        form = ReservaForm()

    return render(request, 'confirmar_reserva.html', {
        'form': form, 'recurso': recurso, 'inicio': inicio
    })

def ayuda(request):
    if request.method == 'POST':
        form = SolicitudAyudaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Solicitud enviada. Un administrador la revisará.')
            return redirect('home')
    else:
        form = SolicitudAyudaForm()
    return render(request, 'ayuda.html', {'form': form})