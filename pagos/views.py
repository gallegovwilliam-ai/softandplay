from django.shortcuts import render, HttpResponse, redirect, Http404
from django.urls import  reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.db.models.query import QuerySet
from django.db.models import Avg, Count, Q
from django.utils.datastructures import MultiValueDictKeyError
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .models import MensajeCarton, MensajeCarton75
from notifications.models import Notification
from cards.models import Impresion, Impresion75
from partidas.models import Partida, Partida75
import datetime
from configuracion.models import Config
from .financial import _payment
from .models import MensajeCarton, MensajeCarton75, Settlement, Settlement75

class PagosList(ListView):
    model = Impresion
    template_name = 'pagos_loteria.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.userprofile.user_type == 'Usuario':
            raise Http404
        return super().dispatch(request, *args, **kwargs) 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bingo"] = Impresion75.objects.filter(ganador=True,pago=False)
        return context      
    def get_queryset(self,*args,**kwargs):
        return Impresion.objects.filter(ganador=True,pago=False)

    
PagosList = PagosList.as_view()

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation


@login_required
def CartonGanador(request,pk):
    try:
        carton = Impresion.objects.select_related('propietario__partida').get(pk=pk)
    except Impresion.DoesNotExist:
        raise Http404
    if not (request.user.is_superuser or request.user == carton.propietario.user):
        raise Http404
    if carton.ganador and not Settlement.objects.filter(partida=carton.propietario.partida).exists():
        return HttpResponse('La partida aún no ha sido liquidada', status=409)
    mensajes = MensajeCarton.objects.filter(carton=carton)
    return render(request,'ver_carton_ganador.html',{'carton':carton,'mensajes':mensajes})


@login_required
def CartonGanador75(request,pk):
    try:
        carton = Impresion75.objects.select_related('propietario__partida').get(pk=pk)
    except Impresion75.DoesNotExist:
        raise Http404
    if not (request.user.is_superuser or request.user == carton.propietario.user):
        raise Http404
    if carton.ganador and not Settlement75.objects.filter(partida=carton.propietario.partida).exists():
        return HttpResponse('La partida aún no ha sido liquidada', status=409)
    mensajes = MensajeCarton75.objects.filter(carton=carton)
    return render(request,'ver_carton_ganador75.html',{'carton':carton,'mensajes':mensajes})


@login_required
def ProcesarPagoCarton(request,pk):
    if request.method != 'POST':
        return HttpResponse(status=405)
    if not request.user.is_superuser:
        raise Http404
    try:
        carton = Impresion.objects.get(pk=pk)
        record, created = _payment(
            carton, request.user, request.POST.get('metodo', '').strip(),
            request.POST.get('datos', '').strip(), request=request
        )
    except Impresion.DoesNotExist:
        raise Http404
    except ValueError as exc:
        return JsonResponse({'ok': False, 'error': str(exc)}, status=400)
    return JsonResponse({'ok': True, 'created': created, 'payment_id': record.pk if record else None})

@login_required
def ProcesarPagoCarton75(request,pk):
    if request.method != 'POST':
        return HttpResponse(status=405)
    if not request.user.is_superuser:
        raise Http404
    try:
        carton = Impresion75.objects.get(pk=pk)
        record, created = _payment(
            carton, request.user, request.POST.get('metodo', '').strip(),
            request.POST.get('datos', '').strip(), is75=True, request=request
        )
    except Impresion75.DoesNotExist:
        raise Http404
    except ValueError as exc:
        return JsonResponse({'ok': False, 'error': str(exc)}, status=400)
    return JsonResponse({'ok': True, 'created': created, 'payment_id': record.pk if record else None})

def Mensaje(request,pk):
    if request.method != 'POST':
        return HttpResponse(status=405)

    try:
        carton = Impresion.objects.get(pk=pk)
    except:
        raise Http404
    if not (request.user.is_superuser or request.user == carton.propietario.user):
        raise Http404
    MensajeCarton.objects.create(user=request.user,carton=carton,mensaje=request.POST.get('mensaje','')[:1000])
    if request.user == carton.propietario.user:
        noti = "Haz recibido un mensaje referente al carton ganador #" + str(pk) + " referente a la partida #" + str(carton.propietario.partida.id)
        Notification.objects.create(user_id=1,notification=noti,url='/pagos/ver-carton/' + str(pk) + '/')
    else:
        noti = "Haz recibido un mensaje referente a tu carton ganador #" + str(pk) + " referente a la partida #" + str(carton.propietario.partida.id)
        Notification.objects.create(user=carton.propietario.user,notification=noti,url='/pagos/ver-carton/' + str(pk) + '/')
    return HttpResponse('ok')

def Mensaje75(request,pk):
    if request.method != 'POST':
        return HttpResponse(status=405)

    try:
        carton = Impresion75.objects.get(pk=pk)
    except:
        raise Http404
    if not (request.user.is_superuser or request.user == carton.propietario.user):
        raise Http404
    MensajeCarton75.objects.create(user=request.user,carton=carton,mensaje=request.POST.get('mensaje','')[:1000])
    if request.user == carton.propietario.user:
        noti = "Haz recibido un mensaje sobre el carton ganador #" + str(pk) + " referente a la partida #" + str(carton.propietario.partida.id)
        Notification.objects.create(user_id=1,notification=noti,url='/pagos/75/ver-carton/' + str(pk) + '/')
    else:
        noti = "Haz recibido un mensaje referente a tu carton ganador #" + str(pk) + " referente a la partida #" + str(carton.propietario.partida.id)
        Notification.objects.create(user=carton.propietario.user,notification=noti,url='/pagos/75/ver-carton/' + str(pk) + '/')
    return HttpResponse('ok')

def MisGanadores(request):
    loterias = Impresion.objects.filter(ganador=True,pago=False,propietario__user=request.user)
    bingos = Impresion75.objects.filter(ganador=True,pago=False,propietario__user=request.user)    
    return render(request,'mis_ganadores.html',{'loterias':loterias,'bingos':bingos})
