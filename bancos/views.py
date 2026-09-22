from django.shortcuts import render, HttpResponse, redirect
from django.urls import  reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.db.models.query import QuerySet
from django.db.models import Avg, Count, Q
from django.db import transaction
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .models import Banco
from .forms import BancoForm
from partidas.models import Partida, Partida75
from django.http import Http404
from django.http import JsonResponse
from django.core import serializers
from cards.models import CabezeraImpre, Impresion, Carton, CabezeraImpre75, Impresion75, Carton75
from clientes.models import Cliente
from notifications.models import Notification
import datetime
from django.utils import timezone
from pagos.reconciliation import register_sale, register_sale75
from cards.services import allocate_cartons

class BancoList(ListView):
    model = Banco
    template_name = 'list_bancos.html'
    def get_queryset(self,*args,**kwargs):
        return Banco.objects.filter(active=True)
BancoList = BancoList.as_view()



class BancoCreate(CreateView):
    model = Banco
    form_class = BancoForm
    template_name = 'add_banco.html'
    success_url = reverse_lazy('list-banco')
    def post(self,*args,**kwargs):
        if not self.request.user.is_superuser:
            raise Http404
        Banco.objects.create(
            moneda=self.request.POST.get('moneda',''),
            corresponsal=self.request.POST.get('corresponsal',''),
            ciudad=self.request.POST.get('ciudad',''),
            codigo_swift=self.request.POST.get('codigo_swift',''),
            banco_benef=self.request.POST.get('banco_benef',''),
            cuenta=self.request.POST.get('cuenta',''),
            beneficiario_final=self.request.POST.get('beneficiario_final',''),
            cuenta_abono=self.request.POST.get('cuenta_abono',''),
            )        
        return redirect(reverse_lazy('list-banco'))
BancoCreate = BancoCreate.as_view()

def BancoDelete(request,pk):
    if request.method != 'POST' or not request.user.is_superuser:
        raise Http404
    Banco.objects.filter(pk=pk).update(active=False)
    return redirect(reverse_lazy('list-banco'))


class BancoUpdate(UpdateView):
    model = Banco
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
    form_class = BancoForm
    template_name = 'update_banco.html'
    success_url = reverse_lazy('list-banco')
BancoUpdate = BancoUpdate.as_view()



def Comprar(request,pk):
    try:
        partida = Partida.objects.get(pk=pk)
        if partida.inicio:
            return redirect('/partidas/juego-en-linea/' + str(pk) + '/')
    except ObjectDoesNotExist:
        raise Http404
    b = Banco.objects.filter(active=True)
    return render(request,'comprar.html',{'partida':partida,'bancos':b,'tipo':'Loteria Mexicana'})


def Comprar75(request,pk):
    try:
        partida = Partida75.objects.get(pk=pk)
        if partida.inicio:
            return redirect('/partidas/75/juego-en-linea/' + str(pk) + '/')
    except ObjectDoesNotExist:
        raise Http404
    b = Banco.objects.filter(active=True)
    return render(request,'comprar75.html',{'partida':partida,'bancos':b,'tipo':'Bingo 75'})


def BancoView(request):
    if not request.user.is_superuser:
        raise Http404
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            b = Banco.objects.get(pk=request.GET['pk'])
            return JsonResponse({
                'moneda':b.moneda,
                'corresponsal':b.corresponsal,
                'ciudad':b.ciudad,
                'codigo_swift':b.codigo_swift,
                'banco_benef':b.banco_benef,
                'cuenta':b.cuenta,
                'beneficiario_final':b.beneficiario_final,
                'cuenta_abono':b.cuenta_abono,                
                },safe=True)
        except ObjectDoesNotExist:
            pass
        return HttpResponse('error')
    else:
        raise Http404


@login_required
@transaction.atomic
def pagarcompra(request,pk):
    if request.method == 'POST':
        try:
            partida = Partida.objects.select_for_update().get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404
        if request.user.userprofile.user_type == 'Usuario':
            try:
                cliente = Cliente.objects.get(user=request.user)
            except ObjectDoesNotExist:
                cliente = Cliente.objects.create(
                        user=request.user,
                        nombre=request.user.first_name,
                        apellido=request.user.last_name,
                        telefono=request.user.userprofile.phone,
                        direccion=request.user.userprofile.address,
                        email = request.user.email
                    )

        else:
            raise Http404
        if partida.inicio or partida.termino:
            return HttpResponse('La partida no admite nuevas ventas', status=409)
        try:
            cantidad = int(request.POST.get('cantidad', 0))
        except (TypeError, ValueError):
            return HttpResponse('Cantidad inválida', status=400)
        if not 1 <= cantidad <= 100:
            return HttpResponse('Cantidad inválida', status=400)
        b = Banco.objects.get(pk = request.POST['banco'])
        CabezeraImpre.objects.create(
            fecha=timezone.localdate(),
            cliente = cliente,
            partida=partida,
            user=request.user,
            cantidad=cantidad,
            banco=b.corresponsal,
            cuenta=request.POST['cuenta'],
            referencia=request.POST['referencia'],
            file = request.FILES['file']
        )
        return HttpResponse('ok')


@login_required
@transaction.atomic
def pagarcompra75(request,pk):
    if request.method == 'POST':
        try:
            partida = Partida75.objects.select_for_update().get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404
        if request.user.userprofile.user_type == 'Usuario':
            try:
                cliente = Cliente.objects.get(user=request.user)
            except ObjectDoesNotExist:
                cliente = Cliente.objects.create(
                        user=request.user,
                        nombre=request.user.first_name,
                        apellido=request.user.last_name,
                        telefono=request.user.userprofile.phone,
                        direccion=request.user.userprofile.address,
                        email = request.user.email
                    )

        else:
            raise Http404
        if partida.inicio or partida.termino:
            return HttpResponse('La partida no admite nuevas ventas', status=409)
        try:
            cantidad = int(request.POST.get('cantidad', 0))
        except (TypeError, ValueError):
            return HttpResponse('Cantidad inválida', status=400)
        if not 1 <= cantidad <= 100:
            return HttpResponse('Cantidad inválida', status=400)
        b = Banco.objects.get(pk = request.POST['banco'])
        CabezeraImpre75.objects.create(
            fecha=timezone.localdate(),
            cliente = cliente,
            partida=partida,
            user=request.user,
            cantidad=cantidad,
            banco=b.corresponsal,
            cuenta=request.POST['cuenta'],
            referencia=request.POST['referencia'],
            file = request.FILES['file']
        )
        return HttpResponse('ok')


def comprasprocesos(request):
    if not request.user.is_superuser:
        raise Http404
    object_list = CabezeraImpre.objects.filter(verficado=False)
    return render(request,'compras-pendientes.html',{'object_list':object_list})

def comprasprocesos75(request):
    if not request.user.is_superuser:
        raise Http404
    object_list = CabezeraImpre75.objects.filter(verficado=False)
    return render(request,'compras-pendientes75.html',{'object_list':object_list})

def deleteCompras(request,pk):
    if request.method != 'POST' or not request.user.is_superuser:
        raise Http404
    CabezeraImpre.objects.filter(pk=pk, verficado=False).delete()
    return redirect(reverse_lazy('compras'))
    

def verCompra(request,pk):
    if not request.user.is_superuser:
        raise Http404
    c = CabezeraImpre.objects.get(pk=pk)
    return render(request,'ver-compra.html',{'compra':c})

def verCompra75(request,pk):
    if not request.user.is_superuser:
        raise Http404
    c = CabezeraImpre75.objects.get(pk=pk)
    return render(request,'ver-compra75.html',{'compra':c})

@transaction.atomic
def aprobarCompra(request,pk):
    if request.method != 'POST' or not request.user.is_superuser:
        raise Http404
    with transaction.atomic():
        cabezera = CabezeraImpre.objects.select_for_update().select_related('partida').get(pk=pk)
        if cabezera.verficado:
            return redirect(reverse_lazy('compras'))
        if cabezera.partida.inicio or cabezera.partida.termino:
            return HttpResponse('La partida no admite nuevas ventas', status=409)
        try:
            cantidad = int(cabezera.cantidad or 0)
        except (TypeError, ValueError):
            return HttpResponse('Cantidad inválida', status=400)
        try:
            allocate_cartons(cabezera.partida, cabezera, cantidad)
        except ValueError:
            return HttpResponse('No hay suficientes cartones disponibles', status=409)
        cabezera.verficado = True
        cabezera.save(update_fields=['verficado'])
        register_sale(cabezera, request.user, request=request)
        Notification.objects.create(user=cabezera.user,notification='Sus cartones para la partida Nº ' + str(cabezera.partida.id) + ' fueron aprobados')
    return redirect(reverse_lazy('compras'))

def aprobarCompra75(request,pk):
    if request.method != 'POST' or not request.user.is_superuser:
        raise Http404
    with transaction.atomic():
        cabezera = CabezeraImpre75.objects.select_for_update().select_related('partida').get(pk=pk)
        if cabezera.verficado:
            return redirect(reverse_lazy('compras75'))
        if cabezera.partida.inicio or cabezera.partida.termino:
            return HttpResponse('La partida no admite nuevas ventas', status=409)
        try:
            cantidad = int(cabezera.cantidad or 0)
        except (TypeError, ValueError):
            return HttpResponse('Cantidad inválida', status=400)
        try:
            allocate_cartons(cabezera.partida, cabezera, cantidad, is75=True)
        except ValueError:
            return HttpResponse('No hay suficientes cartones disponibles', status=409)
        cabezera.verficado = True
        cabezera.save(update_fields=['verficado'])
        register_sale75(cabezera, request.user, request=request)
        Notification.objects.create(user=cabezera.user,notification='Sus cartones para la partida Nº ' + str(cabezera.partida.id) + ' fueron aprobados')
    return redirect(reverse_lazy('compras75'))

def _crear_solicitud_paypal(request, pk, is75=False):
    Model = Partida75 if is75 else Partida
    Header = CabezeraImpre75 if is75 else CabezeraImpre
    if request.method != 'POST':
        return HttpResponse(status=405)
    partida = get_object_or_404(Model.objects.select_for_update(), pk=pk)
    if partida.inicio or partida.termino:
        return HttpResponse('La partida no admite nuevas ventas', status=409)
    if getattr(request.user.userprofile, 'user_type', None) != 'Usuario':
        raise Http404
    try:
        cantidad = int(request.POST.get('cantidad', 0))
    except (TypeError, ValueError):
        return HttpResponse('Cantidad inválida', status=400)
    if not 1 <= cantidad <= 100:
        return HttpResponse('Cantidad inválida', status=400)
    cliente, _ = Cliente.objects.get_or_create(
        user=request.user,
        defaults={
            'nombre': request.user.first_name, 'apellido': request.user.last_name,
            'telefono': request.user.userprofile.phone, 'direccion': request.user.userprofile.address,
            'email': request.user.email,
        },
    )
    header = Header.objects.create(
        fecha=timezone.now().date(), cliente=cliente, partida=partida, user=request.user,
        cantidad=cantidad, banco='paypal', referencia=request.POST.get('referencia','')[:20],
        verficado=False,
    )
    # Nunca entregar cartones por una referencia enviada desde el navegador.
    # La confirmación real del pago debe provenir de un webhook/API del proveedor.
    return HttpResponse('pendiente', status=202)


@login_required
@transaction.atomic
def pagarcomprapaypal(request,pk):
    return _crear_solicitud_paypal(request, pk, False)


@login_required
@transaction.atomic
def pagarcomprapaypal75(request,pk):
    return _crear_solicitud_paypal(request, pk, True)

