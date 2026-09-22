from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import  reverse_lazy
from django.http import Http404
from django.http import JsonResponse
from .models import LotoChance, VentaChance, DetalleVentaChance, TemporalChance
from .forms import LotoChanceForm
from clientes.models import Cliente
import json
import datetime

from django.utils import timezone
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from decimal import Decimal, InvalidOperation
# Create your views here.

class LotoChanceList(ListView):
    model = LotoChance
    template_name = 'list_chance.html'
    def get_queryset(self,*args,**kwargs):
        return LotoChance.objects.filter(active=True)
LotoChanceList = LotoChanceList.as_view()

@method_decorator(login_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class LotoChanceCreateView(CreateView):
    model = LotoChance
    form_class = LotoChanceForm
    template_name = "addChance.html"
    success_url = reverse_lazy('list-chance')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
LotoChanceCreateView = LotoChanceCreateView.as_view()

@method_decorator(login_required, name='dispatch')
class LotoChanceUpdateView(UpdateView):
    model = LotoChance
    form_class = LotoChanceForm
    template_name = "update_chance.html"
    success_url = reverse_lazy('list-chance')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
LotoChanceUpdateView = LotoChanceUpdateView.as_view()

def LotoChanceDelete(request,pk):
    if request.method != 'POST' or not request.user.is_superuser:
        raise Http404
    LotoChance.objects.filter(pk=pk).update(active=False)
    return redirect(reverse_lazy('list-chance'))

def VentaRevendedor(request):
    temporal = TemporalChance.objects.filter(user=request.user)
    if temporal:
        temporal.delete()
    loterias = LotoChance.objects.filter(active=True)
    return render(request,'ventas_revendedores.html',{'loterias':loterias})

def _ajax_staff(request):
    if request.method != 'POST' or request.headers.get('X-Requested-With') != 'XMLHttpRequest' or not request.user.is_staff:
        raise Http404


def EliminarNumero(request,pk):
    _ajax_staff(request)
    deleted, _ = TemporalChance.objects.filter(pk=pk, user=request.user).delete()
    if not deleted:
        return HttpResponse('No encontrado', status=404)
    return HttpResponse(str(pk))


def AsignarNumero(request):
    _ajax_staff(request)
    try:
        loterias = json.loads(request.POST.get('loterias', '[]'))
        numero = str(request.POST.get('numero', '')).strip()
        monto = Decimal(str(request.POST.get('monto', '0'))).quantize(Decimal('0.01'))
    except (TypeError, ValueError, InvalidOperation, json.JSONDecodeError):
        return HttpResponse('Datos inválidos', status=400)
    if not numero.isdigit() or not 0 <= int(numero) <= 9999:
        return HttpResponse('Número inválido', status=400)
    if monto <= 0:
        return HttpResponse('Monto inválido', status=400)
    try:
        ids = list({int(x) for x in loterias})
    except (TypeError, ValueError):
        return HttpResponse('Loterías inválidas', status=400)
    if not ids:
        return HttpResponse('Debe seleccionar al menos una lotería', status=400)
    lotos = list(LotoChance.objects.filter(pk__in=ids, active=True))
    if len(lotos) != len(ids):
        return HttpResponse('Lotería inválida', status=400)
    temporal = TemporalChance.objects.create(
        user=request.user, fecha=timezone.now().date(), numero=numero, monto=str(monto)
    )
    temporal.loterias.set(lotos)
    temporal.total = str((monto * len(lotos)).quantize(Decimal('0.01')))
    temporal.save(update_fields=['total'])
    images = [{'img': str(loto.thumb)} for loto in lotos]
    return JsonResponse([{'numero': numero, 'monto': str(monto), 'total': temporal.total, 'id': temporal.id, 'imgs': images}])


@transaction.atomic
def RealizarVentar(request):
    _ajax_staff(request)
    client_id = request.POST.get('idCliente', '0')
    if client_id and client_id != '0':
        try:
            cliente = Cliente.objects.filter(pk=int(client_id), user=request.user).first()
        except (TypeError, ValueError):
            return HttpResponse('Cliente inválido', status=400)
        if cliente is None:
            return HttpResponse('Cliente no encontrado', status=404)
    else:
        cliente = Cliente.objects.create(
            user=request.user,
            nombre=request.POST.get('nombre', '')[:200],
            telefono=request.POST.get('telefono', '')[:50],
        )
    temporales = list(TemporalChance.objects.filter(user=request.user).prefetch_related('loterias'))
    if not temporales:
        return HttpResponse('No hay números para vender', status=400)
    venta = VentaChance.objects.create(fecha=timezone.now().date(), user=request.user, cliente=cliente)
    for temporal in temporales:
        detalle = DetalleVentaChance.objects.create(propietario=venta, numero=temporal.numero, monto=temporal.monto)
        detalle.loterias.set(temporal.loterias.all())
    TemporalChance.objects.filter(user=request.user).delete()
    return HttpResponse(str(venta.id))
