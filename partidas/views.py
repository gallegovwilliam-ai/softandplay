# -*- encoding: utf-8 -*-
from django.shortcuts import render, HttpResponse, redirect,Http404
from django.urls import  reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.db.models.query import QuerySet
from django.db.models import Avg, Count, Q
from django.db import transaction
from django.utils.datastructures import MultiValueDictKeyError
from .models import Partida, Jugada, Partida75, Jugada75
from clientes.models import Cliente
from cards.models import Impresion, Impresion75
from .forms import PartidaForm, Partida75Form
import datetime
from django.utils import timezone
import random
from configuracion.models import Config
import json
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from pagos.settlement import settle_partida, settle_partida75
from .models import PartidaSequence
from .validation import validate_partida_post


def next_partida_number(fecha, tipo, model):
    """Obtiene un consecutivo diario serializado en PostgreSQL/SQLite."""
    with transaction.atomic():
        ultimo = model.objects.filter(fecha=fecha).order_by('-partida').values_list('partida', flat=True).first() or 0
        seq, _ = PartidaSequence.objects.get_or_create(fecha=fecha, tipo=tipo, defaults={'ultimo_numero': int(ultimo)})
        seq = PartidaSequence.objects.select_for_update().get(pk=seq.pk)
        if seq.ultimo_numero < int(ultimo):
            seq.ultimo_numero = int(ultimo)
        seq.ultimo_numero += 1
        seq.save(update_fields=['ultimo_numero'])
        return seq.ultimo_numero

#loto mexibcana
class PartidaList(ListView):
    model = Partida
    template_name = 'list_partidas.html'
    def get_queryset(self):
        if self.kwargs['tag'] == 'en-espera':
            return Partida.objects.filter(inicio=False,termino=False,fecha__gte=timezone.localdate()).order_by('fecha')
        if self.kwargs['tag'] == 'en-juego':
            return Partida.objects.filter(inicio=True,termino=False,fecha__gte=timezone.localdate()).order_by('fecha','id')
        if self.kwargs['tag'] == 'finalizadas':
            return Partida.objects.filter(inicio=True,termino=True,fecha__gte=timezone.localdate()).order_by('fecha','id')           
        return Partida.objects.filter(inicio=False,termino=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']
        return context
PartidaList = PartidaList.as_view()

# bingo 75
class PartidaList75(ListView):
    model = Partida75
    template_name = 'list_partidas75.html'
    def get_queryset(self):
        if self.kwargs['tag'] == 'en-espera':
            return Partida75.objects.filter(inicio=False,termino=False,fecha__gte=timezone.localdate()).order_by('fecha')
        if self.kwargs['tag'] == 'en-juego':
            return Partida75.objects.filter(inicio=True,termino=False,fecha__gte=timezone.localdate()).order_by('fecha','id')
        if self.kwargs['tag'] == 'finalizadas':
            return Partida75.objects.filter(inicio=True,termino=True,fecha__gte=timezone.localdate()).order_by('fecha','id')           
        return Partida75.objects.filter(inicio=False,termino=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']
        return context
PartidaList75 = PartidaList75.as_view()


#loto mexibcana
class PartidaCreate(CreateView):
    model = Partida
    form_class = PartidaForm
    template_name = 'add_partida.html'
    success_url = reverse_lazy('partida-list')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        return super(PartidaCreate, self).dispatch(request, *args, **kwargs)
    def post(self,request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        try:
            validate_partida_post(request.POST)
        except ValueError as exc:
            return HttpResponse(str(exc), status=400)
        numero_partida = next_partida_number(request.POST['fecha'], PartidaSequence.TIPO_LOTERIA, Partida)
        figura_1 = request.POST.get('figura_1',False) if request.POST.get('figura_1',False) is False else True
        figura_2 = request.POST.get('figura_2',False) if request.POST.get('figura_2',False) is False else True
        figura_3 = request.POST.get('figura_3',False) if request.POST.get('figura_3',False) is False else True
        figura_4 = request.POST.get('figura_4',False) if request.POST.get('figura_4',False) is False else True
        figura_5 = request.POST.get('figura_5',False) if request.POST.get('figura_5',False) is False else True
        figura_6 = request.POST.get('figura_6',False) if request.POST.get('figura_6',False) is False else True
        figura_7 = request.POST.get('figura_7',False) if request.POST.get('figura_7',False) is False else True
        figura_8 = request.POST.get('figura_8',False) if request.POST.get('figura_8',False) is False else True
        figura_9 = request.POST.get('figura_9',False) if request.POST.get('figura_9',False) is False else True
        figura_10 = request.POST.get('figura_10',False) if request.POST.get('figura_10',False) is False else True
        partida = Partida.objects.create(fecha=request.POST['fecha'],partida=numero_partida, descripcion =  request.POST['descripcion'], figura_1=figura_1, figura_2=figura_2, figura_3=figura_3, figura_4=figura_4, figura_5=figura_5, figura_6=figura_6, figura_7=figura_7,figura_8 = figura_8, figura_9=figura_9, figura_10=figura_10, porciento_1=request.POST.get('porciento_1','0'),porciento_2=request.POST.get('porciento_2','0'),porciento_3=request.POST.get('porciento_3','0'),porciento_4=request.POST.get('porciento_4','0'),porciento_5=request.POST.get('porciento_5','0'),porciento_6=request.POST.get('porciento_6','0'),porciento_7=request.POST.get('porciento_7','0'),porciento_8=request.POST.get('porciento_8','0'),porciento_9=request.POST.get('porciento_9','0'),porciento_10=request.POST.get('porciento_10','0'),monto_carton=request.POST.get('monto_carton','0'))
        partida.save()
        return redirect(reverse_lazy('partida-list',kwargs={'tag': 'en-espera'}))
PartidaCreate = PartidaCreate.as_view()

# bingo 75
class Partida75Create(CreateView):
    model = Partida75
    form_class = Partida75Form
    template_name = 'add_partida75.html'
    success_url = reverse_lazy('partida75-list')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        return super(Partida75Create, self).dispatch(request, *args, **kwargs)
    def post(self,request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        try:
            validate_partida_post(request.POST)
        except ValueError as exc:
            return HttpResponse(str(exc), status=400)
        numero_partida = next_partida_number(request.POST['fecha'], PartidaSequence.TIPO_BINGO75, Partida75)
        figura_1 = request.POST.get('figura_1',False) if request.POST.get('figura_1',False) is False else True
        figura_2 = request.POST.get('figura_2',False) if request.POST.get('figura_2',False) is False else True
        figura_3 = request.POST.get('figura_3',False) if request.POST.get('figura_3',False) is False else True
        figura_4 = request.POST.get('figura_4',False) if request.POST.get('figura_4',False) is False else True
        figura_5 = request.POST.get('figura_5',False) if request.POST.get('figura_5',False) is False else True
        figura_6 = request.POST.get('figura_6',False) if request.POST.get('figura_6',False) is False else True
        figura_7 = request.POST.get('figura_7',False) if request.POST.get('figura_7',False) is False else True
        figura_8 = request.POST.get('figura_8',False) if request.POST.get('figura_8',False) is False else True
        figura_9 = request.POST.get('figura_9',False) if request.POST.get('figura_9',False) is False else True
        figura_10 = request.POST.get('figura_10',False) if request.POST.get('figura_10',False) is False else True
        partida = Partida75.objects.create(fecha=request.POST['fecha'],partida=numero_partida, descripcion =  request.POST['descripcion'], figura_1=figura_1, figura_2=figura_2, figura_3=figura_3, figura_4=figura_4, figura_5=figura_5, figura_6=figura_6, figura_7=figura_7,figura_8 = figura_8, figura_9=figura_9, figura_10=figura_10, porciento_1=request.POST.get('porciento_1','0'),porciento_2=request.POST.get('porciento_2','0'),porciento_3=request.POST.get('porciento_3','0'),porciento_4=request.POST.get('porciento_4','0'),porciento_5=request.POST.get('porciento_5','0'),porciento_6=request.POST.get('porciento_6','0'),porciento_7=request.POST.get('porciento_7','0'),porciento_8=request.POST.get('porciento_8','0'),porciento_9=request.POST.get('porciento_9','0'),porciento_10=request.POST.get('porciento_10','0'),monto_carton=request.POST.get('monto_carton','0'))
        partida.save()
        return redirect(reverse_lazy('partida75-list',kwargs={'tag': 'en-espera'}))
Partida75Create = Partida75Create.as_view()


#looto mexicana
class PartidaUpdate(UpdateView):
    model = Partida
    form_class = PartidaForm
    template_name = 'update_partida.html'
    success_url = reverse_lazy('partida-list')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        return super(PartidaUpdate, self).dispatch(request, *args, **kwargs)
    def post(self,request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        try:
            validate_partida_post(request.POST)
        except ValueError as exc:
            return HttpResponse(str(exc), status=400)
        current = Partida.objects.filter(pk=kwargs['pk']).first()
        if not current:
            raise Http404
        if current.inicio or current.termino:
            return HttpResponse('No se puede modificar una partida iniciada o finalizada', status=409)
        figura_1 = request.POST.get('figura_1',False) if request.POST.get('figura_1',False) is False else True
        figura_2 = request.POST.get('figura_2',False) if request.POST.get('figura_2',False) is False else True
        figura_3 = request.POST.get('figura_3',False) if request.POST.get('figura_3',False) is False else True
        figura_4 = request.POST.get('figura_4',False) if request.POST.get('figura_4',False) is False else True
        figura_5 = request.POST.get('figura_5',False) if request.POST.get('figura_5',False) is False else True
        figura_6 = request.POST.get('figura_6',False) if request.POST.get('figura_6',False) is False else True
        figura_7 = request.POST.get('figura_7',False) if request.POST.get('figura_7',False) is False else True
        figura_8 = request.POST.get('figura_8',False) if request.POST.get('figura_8',False) is False else True
        figura_9 = request.POST.get('figura_9',False) if request.POST.get('figura_9',False) is False else True
        figura_10 = request.POST.get('figura_10',False) if request.POST.get('figura_10',False) is False else True
        partida = Partida.objects.filter(pk=kwargs['pk']).update(fecha=request.POST['fecha'], descripcion =  request.POST['descripcion'], figura_1=figura_1, figura_2=figura_2, figura_3=figura_3, figura_4=figura_4, figura_5=figura_5, figura_6=figura_6, figura_7=figura_7,figura_8 = figura_8, figura_9=figura_9, figura_10=figura_10, porciento_1=request.POST.get('porciento_1','0'),porciento_2=request.POST.get('porciento_2','0'),porciento_3=request.POST.get('porciento_3','0'),porciento_4=request.POST.get('porciento_4','0'),porciento_5=request.POST.get('porciento_5','0'),porciento_6=request.POST.get('porciento_6','0'),porciento_7=request.POST.get('porciento_7','0'),porciento_8=request.POST.get('porciento_8','0'),porciento_9=request.POST.get('porciento_9','0'),porciento_10=request.POST.get('porciento_10','0'),monto_carton=request.POST.get('monto_carton','0'))
        return redirect(reverse_lazy('partida-list',kwargs={'tag': 'en-espera'}))
PartidaUpdate = PartidaUpdate.as_view()

#bingo 75
class Partida75Update(UpdateView):
    model = Partida75
    form_class = Partida75Form
    template_name = 'update_partida75.html'
    success_url = reverse_lazy('partida75-list')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        return super(Partida75Update, self).dispatch(request, *args, **kwargs)
    def post(self,request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        try:
            validate_partida_post(request.POST)
        except ValueError as exc:
            return HttpResponse(str(exc), status=400)
        current = Partida75.objects.filter(pk=kwargs['pk']).first()
        if not current:
            raise Http404
        if current.inicio or current.termino:
            return HttpResponse('No se puede modificar una partida iniciada o finalizada', status=409)
        figura_1 = request.POST.get('figura_1',False) if request.POST.get('figura_1',False) is False else True
        figura_2 = request.POST.get('figura_2',False) if request.POST.get('figura_2',False) is False else True
        figura_3 = request.POST.get('figura_3',False) if request.POST.get('figura_3',False) is False else True
        figura_4 = request.POST.get('figura_4',False) if request.POST.get('figura_4',False) is False else True
        figura_5 = request.POST.get('figura_5',False) if request.POST.get('figura_5',False) is False else True
        figura_6 = request.POST.get('figura_6',False) if request.POST.get('figura_6',False) is False else True
        figura_7 = request.POST.get('figura_7',False) if request.POST.get('figura_7',False) is False else True
        figura_8 = request.POST.get('figura_8',False) if request.POST.get('figura_8',False) is False else True
        figura_9 = request.POST.get('figura_9',False) if request.POST.get('figura_9',False) is False else True
        figura_10 = request.POST.get('figura_10',False) if request.POST.get('figura_10',False) is False else True
        partida = Partida75.objects.filter(pk=kwargs['pk']).update(fecha=request.POST['fecha'], descripcion =  request.POST['descripcion'], figura_1=figura_1, figura_2=figura_2, figura_3=figura_3, figura_4=figura_4, figura_5=figura_5, figura_6=figura_6, figura_7=figura_7,figura_8 = figura_8, figura_9=figura_9, figura_10=figura_10,porciento_1=request.POST.get('porciento_1','0'),porciento_2=request.POST.get('porciento_2','0'),porciento_3=request.POST.get('porciento_3','0'),porciento_4=request.POST.get('porciento_4','0'),porciento_5=request.POST.get('porciento_5','0'),porciento_6=request.POST.get('porciento_6','0'),porciento_7=request.POST.get('porciento_7','0'),porciento_8=request.POST.get('porciento_8','0'),porciento_9=request.POST.get('porciento_9','0'),porciento_10=request.POST.get('porciento_10','0'),monto_carton=request.POST.get('monto_carton','0'))
        return redirect(reverse_lazy('partida75-list',kwargs={'tag': 'en-espera'}))
Partida75Update = Partida75Update.as_view()

#loteria mexicana
def DeletePartida(request,pk):
    if request.method != 'POST':
        return HttpResponse(status=405)
    if request.user.is_superuser:
        partida = Partida.objects.filter(pk=pk).first()
        if not partida:
            raise Http404
        if partida.inicio or partida.termino:
            return HttpResponse('No se puede eliminar una partida iniciada o finalizada', status=409)
        partida.delete()
        return redirect(reverse_lazy('partida-list',kwargs={'tag':'en-espera'}))
    else:
        raise Http404

#bingo 75
def DeletePartida75(request,pk):
    if request.method != 'POST':
        return HttpResponse(status=405)
    if request.user.is_superuser:
        partida = Partida75.objects.filter(pk=pk).first()
        if not partida:
            raise Http404
        if partida.inicio or partida.termino:
            return HttpResponse('No se puede eliminar una partida iniciada o finalizada', status=409)
        partida.delete()
        return redirect(reverse_lazy('partida75-list',kwargs={'tag':'en-espera'}))
    else:
        raise Http404

#loteria mexicana
class lobby(ListView):
    model = Partida
    template_name = 'tablero/lobby.html'
    def dispatch(self,  *args, **kwargs):
        try:
            Partida.objects.filter(fecha__lt = datetime.date.today(),inicio=True,termino=False).update(termino=True)
            partida = Partida.objects.get(inicio=True, termino=False)
        except ObjectDoesNotExist:
            partida = None
        if partida:
            return redirect(reverse_lazy('tablero',kwargs={'pk': partida.pk}))
        return super().dispatch(*args, **kwargs)
    def get_queryset(self, *args,**kwargs):
        return Partida.objects.filter(fecha=timezone.localdate(),termino=False)
lobby = lobby.as_view()

#bingo 75
class lobby75(ListView):
    model = Partida75
    template_name = 'tablero/lobby75.html'
    def dispatch(self,  *args, **kwargs):
        try:
            Partida75.objects.filter(fecha__lt = datetime.date.today(),inicio=True,termino=False).update(termino=True)
            partida = Partida75.objects.get(inicio=True, termino=False)
        except ObjectDoesNotExist:
            partida = None
        if partida:
            return redirect(reverse_lazy('tablero75',kwargs={'pk': partida.pk}))
        return super().dispatch(*args, **kwargs)
    def get_queryset(self, *args,**kwargs):
        return Partida75.objects.filter(fecha=timezone.localdate(),termino=False)
lobby75 = lobby75.as_view()

#loto mexicana
def Tablero(request,pk):
    fondo = Config.objects.get(pk=1)
    balotas = set(range(1,55))
    partida = Partida.objects.select_for_update().get(pk=pk)
    if not partida or partida.termino:
        return redirect(reverse_lazy('lobby-partida'))

    jugada = Jugada.objects.filter(partida=partida)
    
    #define el numero de balotas que han salido
    balotasJugadas = 0
    
    if jugada:
        for j in jugada:
            balotas.remove(int(j.balota))
            balotasJugadas = balotasJugadas + 1

    #cartones en sala
    cartonensala = Impresion.objects.filter(propietario__partida_id=partida.id).count()    

    #CARTONES VENDIDOS GENERAL
    cartonvendidos = Impresion.objects.filter(propietario__partida_id=partida.id).count()    
    
    if cartonvendidos == 0:
        partida.inicio = False
        partida.save()
        return render(request,'tablero/novendidos.html',{})

    #SABER SI ES AUTOMATICO O MANUAL SEGUN EL LMODULO CONFIGURACION
    #TipoP = Configuracion.objects.get(pk=1)

    if not partida.inicio:
        return render(request,'tablero/inicio.html',{'cartonensala':cartonensala,'cartonvendidos':cartonvendidos,'partida':partida})


    #ULTIMAS 5 BALOTAS
    ultimas5 =Jugada.objects.filter(partida=partida).order_by('-id')[:5]
   

    #SI ES SUPER USER VA AL TABLERO DE ADMIN
    if request.user.is_superuser:
        resellers = User.objects.filter(is_active=True,userprofile__user_type="Revendedor")
        revendedores = []
        partida_id = partida.id
        for r in resellers:
            revendedores.append({'user':r,'vendidos': Impresion.objects.filter(propietario__partida = partida,propietario__user=r).count()})
        return render(request,'tablero/TableroAdmin.html',{'ultimas5':ultimas5,'numeros':jugada,'balotasJugadas':balotasJugadas,'cartonensala':cartonensala,'cartonvendidos':cartonvendidos,'partidanum':partida.id,'f1':partida.figura_1,'f2':partida.figura_2,'f3':partida.figura_3,'f4':partida.figura_4,'f5':partida.figura_5,'f6':partida.figura_6,'f7':partida.figura_7,'f8':partida.figura_8,'f9':partida.figura_9,'f10':partida.figura_10,'rango': range(1,55),'revendedores':revendedores,'idCliente':1,'fondo_pantalla_mexicana':fondo.fondo_pantalla_mexicana})
    else:
        if request.user.userprofile.user_type == 'Usuario':
            cli = Cliente.objects.get(user=request.user)
            idCliente = cli.id
        else:
            idCliente = 0
        return render(request,'tablero/tablero.html',{'ultimas5':ultimas5,'numeros':jugada,'balotasJugadas':balotasJugadas,'cartonensala':cartonensala,'cartonvendidos':cartonvendidos,'partidanum':partida.id, 'idCliente':idCliente,'fondo_pantalla_mexicana':fondo.fondo_pantalla_mexicana})


#bingo 75
def Tablero75(request,pk):
    fondo = Config.objects.get(pk=1)
    balotas = set(range(1,76))
    partida = Partida75.objects.select_for_update().get(pk=pk)
    if not partida or partida.termino:
        return redirect(reverse_lazy('lobby-partida75'))

    jugada = Jugada75.objects.filter(partida=partida)
    
    #define el numero de balotas que han salido
    balotasJugadas = 0
    
    if jugada:
        for j in jugada:
            balotas.remove(int(j.balota))
            balotasJugadas = balotasJugadas + 1

    #cartones en sala
    cartonensala = Impresion75.objects.filter(propietario__partida_id=partida.id).count()    

    #CARTONES VENDIDOS GENERAL
    cartonvendidos = Impresion75.objects.filter(propietario__partida_id=partida.id).count()    
    
    if cartonvendidos == 0:
        partida.inicio = False
        partida.save()
        return render(request,'tablero/novendidos.html',{})

    #SABER SI ES AUTOMATICO O MANUAL SEGUN EL LMODULO CONFIGURACION
    #TipoP = Configuracion.objects.get(pk=1)

    if not partida.inicio:
        return render(request,'tablero/inicio.html',{'cartonensala':cartonensala,'cartonvendidos':cartonvendidos,'partida':partida})


    #ULTIMAS 5 BALOTAS
    ultimas5 =Jugada75.objects.filter(partida=partida).order_by('-id')[:5]
   

    #SI ES SUPER USER VA AL TABLERO DE ADMIN
    if request.user.is_superuser:
        resellers = User.objects.filter(is_active=True,userprofile__user_type="Revendedor")
        revendedores = []
        partida_id = partida.id
        for r in resellers:
            revendedores.append({'user':r,'vendidos': Impresion75.objects.filter(propietario__partida = partida,propietario__user=r).count()})
        return render(request,'tablero/TableroAdmin75.html',{'ultimas5':ultimas5,'numeros':jugada,'balotasJugadas':balotasJugadas,'cartonensala':cartonensala,'cartonvendidos':cartonvendidos,'partidanum':partida.id,'f1':partida.figura_1,'f2':partida.figura_2,'f3':partida.figura_3,'f4':partida.figura_4,'f5':partida.figura_5,'f6':partida.figura_6,'f7':partida.figura_7,'f8':partida.figura_8,'f9':partida.figura_9,'f10':partida.figura_10,'rango': range(1,76),'revendedores':revendedores, 'idCliente':1,'fondo_pantalla_bingo':fondo.fondo_pantalla_bingo})
    else:
        if request.user.userprofile.user_type == 'Usuario':
            cli = Cliente.objects.get(user=request.user)
            idCliente = cli.id
        else:
            idCliente = 0
        return render(request,'tablero/tablero75.html',{'ultimas5':ultimas5,'numeros':jugada,'balotasJugadas':balotasJugadas,'cartonensala':cartonensala,'cartonvendidos':cartonvendidos,'partidanum':partida.id, 'idCliente':idCliente,'fondo_pantalla_bingo':fondo.fondo_pantalla_bingo})



#loteria mexicana
@transaction.atomic
def inicarPartida(request,pk):
    if request.method != 'POST':
        return HttpResponse(status=405)
    if not request.user.is_superuser:
        raise Http404
    try:
        partida = Partida.objects.select_for_update().get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    if partida.termino:
        return HttpResponse('La partida ya terminó', status=409)
    if partida.inicio:
        return HttpResponse('La partida ya está iniciada', status=409)
    partida.inicio = True
    partida.save(update_fields=['inicio'])
    return HttpResponse('ok')

#Bingo 75
@transaction.atomic
def inicarPartida75(request,pk):
    if request.method != 'POST':
        return HttpResponse(status=405)
    if not request.user.is_superuser:
        raise Http404
    try:
        partida = Partida75.objects.select_for_update().get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    if partida.termino:
        return HttpResponse('La partida ya terminó', status=409)
    if partida.inicio:
        return HttpResponse('La partida ya está iniciada', status=409)
    partida.inicio = True
    partida.save(update_fields=['inicio'])
    return HttpResponse('ok')

def realtime(data):
    channel_layer = get_channel_layer()
    data = data       # Trigger message sent to group
    async_to_sync(channel_layer.group_send)(
        'partida',  # Group Name, Should always be string
        {
            "type": "notify",   # Custom Function written in the consumers.py
            "text": data,
        },
    )   

from django.core import serializers
from django.template.loader import render_to_string
from configuracion.models import Config
#loto mexivcana
@transaction.atomic
def JuegoEnLinea(request,pk):
    if not request.user.is_superuser:
        raise Http404
    balotas = set(range(1,55))
    salidos = list()
    partida = Partida.objects.select_for_update().get(pk=pk)
    if partida.termino:
        return redirect(reverse_lazy('lobby-partida'))
    
    if partida.figura_1 == partida.ganador_1 and partida.figura_2 == partida.ganador_2 and partida.figura_3 == partida.ganador_3 and partida.figura_4 == partida.ganador_4 and partida.figura_5 == partida.ganador_5 and partida.figura_6 == partida.ganador_6 and partida.figura_7 == partida.ganador_7 and partida.figura_8 == partida.ganador_8 and partida.figura_9 == partida.ganador_9 and partida.figura_10 == partida.ganador_10:
        param = {'ganador':'termino'}
        partida.termino = True
        partida.save(update_fields=['termino'])
        settle_partida(partida.pk, request.user, request=request)
        realtime(param)
        return JsonResponse(param)
    balotasJugadas=0
    #SACO LAS BALOTAS QUE YA SALIERON DEL ARREGLO O LISTA
    jugada = Jugada.objects.filter(partida=partida)
    if jugada:
        for j in jugada:
            balotas.remove(int(j.balota))
            salidos.append(int(j.balota))
            balotasJugadas = balotasJugadas + 1
    #SACO LA BALOTA DE LA LISTA
    balota = random.choice(list(balotas))
    salidos.append(balota)
    salidos.append(0)
    #VALIDO SI NO HAY LA MISMA BALOTA PARA PARTIDA Y GUARDO
    j = Jugada.objects.filter(partida=partida,balota=balota)
    if not j:
        c = Jugada.objects.create(partida_id=partida.id, balota=balota)  
    ultimas5 =Jugada.objects.filter(partida=partida).order_by('-id')[:5]
    ultimas5 = serializers.serialize('json', list(ultimas5), fields=('balota'))        
    #FIGURA 1 LINEA AL AZAR
    cartones = []
    config = Config.objects.get(pk=1)
    if partida.figura_1 == True:
        if partida.ganador_1 == False:
            lv1 =Impresion.objects.filter(propietario__partida_id=partida.id, carton__l1_1__in=salidos,carton__l2_1__in=salidos,carton__l3_1__in=salidos,carton__l4_1__in=salidos,) 
            lv2 =Impresion.objects.filter(propietario__partida_id=partida.id, carton__l1_2__in=salidos,carton__l2_2__in=salidos,carton__l3_2__in=salidos,carton__l4_2__in=salidos,) 
            lv3 =Impresion.objects.filter(propietario__partida_id=partida.id, carton__l1_3__in=salidos,carton__l2_3__in=salidos,carton__l3_3__in=salidos,carton__l4_3__in=salidos,) 
            lv4 =Impresion.objects.filter(propietario__partida_id=partida.id, carton__l1_4__in=salidos,carton__l2_4__in=salidos,carton__l3_4__in=salidos,carton__l4_4__in=salidos,) 
            lh1 = Impresion.objects.filter(propietario__partida_id=partida.id, carton__l1_1__in=salidos,carton__l1_2__in=salidos,carton__l1_3__in=salidos,carton__l1_4__in=salidos,)
            lh2 = Impresion.objects.filter(propietario__partida_id=partida.id, carton__l2_1__in=salidos,carton__l2_2__in=salidos,carton__l2_3__in=salidos,carton__l2_4__in=salidos,)       
            lh3 = Impresion.objects.filter(propietario__partida_id=partida.id, carton__l3_1__in=salidos,carton__l3_2__in=salidos,carton__l3_3__in=salidos,carton__l3_4__in=salidos,)       
            lh4 = Impresion.objects.filter(propietario__partida_id=partida.id, carton__l4_1__in=salidos,carton__l4_2__in=salidos,carton__l4_3__in=salidos,carton__l4_4__in=salidos,)       
            ban = False
            if lv1:
                ban = True
                for p in lv1: 
                    p.ganador_1 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                    cartones.append(p)

            if lv2:
                ban = True
                for p in lv2: 
                    p.ganador_1 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                    cartones.append(p)

            if lv3:
                ban = True
                for p in lv3: 
                    p.ganador_1 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                    cartones.append(p)

            if lv4:
                ban = True
                for p in lv4: 
                    p.ganador_1 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                    cartones.append(p)
            if lh1:
                ban = True
                for p in lh1: 
                    p.ganador_1 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                    cartones.append(p)

            if lh2:
                ban = True
                for p in lh2: 
                    p.ganador_1 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                    cartones.append(p)

            if lh3:
                ban = True
                for p in lh3: 
                    p.ganador_1 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                    cartones.append(p)

            if lh4:
                ban = True
                for p in lh4: 
                    p.ganador_1 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                    cartones.append(p)

            if ban:
                partida.ganador_1=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores.html',{'cartones':cartones,'figura':'Linea al Azar','fondo':config.fondo_carton_lotoMX })
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param)

    #FIGURA 2 LINEA vertical 1
    if partida.figura_2 == True:
        if partida.ganador_2 == False:
            po = Impresion.objects.filter(propietario__partida_id=partida.id, carton__l1_1__in=salidos,carton__l2_1__in=salidos,carton__l3_1__in=salidos,carton__l4_1__in=salidos,) 
            if po:
                for p in po: 
                    p.ganador_2 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                partida.ganador_2=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores.html',{'cartones':po,'figura':'Primera Linea Vertical','fondo':config.fondo_carton_lotoMX },request)
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param)

    #FIGURA 3 LINEA vertical 2
    if partida.figura_3 == True:
        if partida.ganador_3 == False:
            po = Impresion.objects.filter(propietario__partida_id=partida.id, carton__l1_2__in=salidos,carton__l2_2__in=salidos,carton__l3_2__in=salidos,carton__l4_2__in=salidos,) 
            if po:
                for p in po: 
                    p.ganador_3 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                partida.ganador_3=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores.html',{'cartones':po,'figura':'Segunda Linea Vertical','fondo':config.fondo_carton_lotoMX },request)
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param) 
    #FIGURA 4 LINEA vertical 3
    if partida.figura_4 == True:
        if partida.ganador_4 == False:
            po = Impresion.objects.filter(propietario__partida_id=partida.id, carton__l1_3__in=salidos,carton__l2_3__in=salidos,carton__l3_3__in=salidos,carton__l4_3__in=salidos,) 
            if po:
                for p in po: 
                    p.ganador_4 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                partida.ganador_4=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores.html',{'cartones':po,'figura':'Tercera Linea Vertical','fondo':config.fondo_carton_lotoMX },request)
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param) 

    #FIGURA 5 LINEA vertical 4
    if partida.figura_5 == True:
        if partida.ganador_5 == False:
            po = Impresion.objects.filter(propietario__partida_id=partida.id, carton__l1_4__in=salidos,carton__l2_4__in=salidos,carton__l3_4__in=salidos,carton__l4_4__in=salidos,) 
            if po:
                for p in po: 
                    p.ganador_5 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                partida.ganador_5=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores.html',{'cartones':po,'figura':'Cuarta Linea Vertical','fondo':config.fondo_carton_lotoMX },request)
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param) 

    #FIGURA 6 LINEA Horizontal 1
    if partida.figura_6 == True:
        if partida.ganador_6 == False:
            po = Impresion.objects.filter(propietario__partida_id=partida.id, carton__l1_1__in=salidos,carton__l1_2__in=salidos,carton__l1_3__in=salidos,carton__l1_4__in=salidos,)
            if po:
                for p in po: 
                    p.ganador_6 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                partida.ganador_6=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores.html',{'cartones':po,'figura':'Primera Linea Horizontal','fondo':config.fondo_carton_lotoMX },request)
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param) 
                

    #FIGURA 7 LINEA Horizontal 2
    if partida.figura_7 == True:
        if partida.ganador_7 == False:
            po = Impresion.objects.filter(propietario__partida_id=partida.id, carton__l2_1__in=salidos,carton__l2_2__in=salidos,carton__l2_3__in=salidos,carton__l2_4__in=salidos,)
            if po:
                for p in po: 
                    p.ganador_7 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                partida.ganador_7=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores.html',{'cartones':po,'figura':'Segunda Linea Horizontal','fondo':config.fondo_carton_lotoMX },request)
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param) 
                
    #FIGURA 8 LINEA Horizontal 3
    if partida.figura_8 == True:
        if partida.ganador_8 == False:
            po = Impresion.objects.filter(propietario__partida_id=partida.id, carton__l3_1__in=salidos,carton__l3_2__in=salidos,carton__l3_3__in=salidos,carton__l3_4__in=salidos,)
            if po:
                for p in po: 
                    p.ganador_8 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                partida.ganador_8=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores.html',{'cartones':po,'figura':'Tercera Linea Horizontal','fondo':config.fondo_carton_lotoMX },request)
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param) 
                
    #FIGURA 9 LINEA Horizontal 9
    if partida.figura_9 == True:
        if partida.ganador_9 == False:
            po =Impresion.objects.filter(propietario__partida_id=partida.id, carton__l4_1__in=salidos,carton__l4_2__in=salidos,carton__l4_3__in=salidos,carton__l4_4__in=salidos,)
            if po:
                for p in po: 
                    p.ganador_9 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                partida.ganador_9=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores.html',{'cartones':po,'figura':'Cuarta Linea Horizontal','fondo':config.fondo_carton_lotoMX },request)
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param) 
    #FIGURA 10 tabla llena
    if partida.figura_10 == True:
        if partida.ganador_10 == False:
            po =Impresion.objects.filter(
                propietario__partida_id=partida.id, 
                carton__l1_1__in=salidos,
                carton__l2_1__in=salidos,
                carton__l3_1__in=salidos,
                carton__l4_1__in=salidos,
                carton__l1_2__in=salidos,
                carton__l2_2__in=salidos,
                carton__l3_2__in=salidos,
                carton__l4_2__in=salidos,
                carton__l1_3__in=salidos,
                carton__l2_3__in=salidos,
                carton__l3_3__in=salidos,
                carton__l4_3__in=salidos,
                carton__l1_4__in=salidos,
                carton__l2_4__in=salidos,
                carton__l3_4__in=salidos,
                carton__l4_4__in=salidos,)
            if po:
                for p in po: 
                    p.ganador_10 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                partida.ganador_10=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores.html',{'cartones':po,'figura':'Tabla Llena','fondo':config.fondo_carton_lotoMX },request)
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param) 

    param = {'ganador':'none','balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
    realtime(param)
    return JsonResponse(param)

#bingo 75
@transaction.atomic
def JuegoEnLinea75(request,pk):
    if not request.user.is_superuser:
        raise Http404
    balotas = set(range(1,76))
    salidos = list()
    partida = Partida75.objects.select_for_update().get(pk=pk)
    if partida.termino:
        return redirect(reverse_lazy('lobby-partida75'))
    
    if partida.figura_1 == partida.ganador_1 and partida.figura_2 == partida.ganador_2 and partida.figura_3 == partida.ganador_3 and partida.figura_4 == partida.ganador_4 and partida.figura_5 == partida.ganador_5 and partida.figura_6 == partida.ganador_6 and partida.figura_7 == partida.ganador_7 and partida.figura_8 == partida.ganador_8 and partida.figura_9 == partida.ganador_9 and partida.figura_10 == partida.ganador_10:
        param = {'ganador':'termino'}
        partida.termino = True
        partida.save(update_fields=['termino'])
        settle_partida75(partida.pk, request.user, request=request)
        realtime(param)
        return JsonResponse(param)
    balotasJugadas=0
    #SACO LAS BALOTAS QUE YA SALIERON DEL ARREGLO O LISTA
    jugada = Jugada75.objects.filter(partida=partida)
    if jugada:
        for j in jugada:
            balotas.remove(int(j.balota))
            salidos.append(int(j.balota))
            balotasJugadas = balotasJugadas + 1
    #SACO LA BALOTA DE LA LISTA
    print(request.GET.get('numeroSelecto',None))
    print(salidos)
    numero_selecto = request.GET.get('numeroSelecto')
    if numero_selecto:
        try:
            balota = int(numero_selecto)
        except (TypeError, ValueError):
            return JsonResponse({'error': 'Balota inválida'}, status=400)
        if balota not in balotas:
            return JsonResponse({'error': 'La balota ya salió o está fuera de rango'}, status=409)
    else:
        balota = random.choice(list(balotas))
    salidos.append(balota)
    salidos.append(0)
    #VALIDO SI NO HAY LA MISMA BALOTA PARA PARTIDA Y GUARDO
    j = Jugada75.objects.filter(partida=partida,balota=balota)
    if not j:
        c = Jugada75.objects.create(partida_id=partida.id, balota=balota)  
    ultimas5 =Jugada75.objects.filter(partida=partida).order_by('-id')[:5]
    ultimas5 = serializers.serialize('json', list(ultimas5), fields=('balota'))        

    #FIGURA 1 LINEA B
    cartones = []
    if partida.figura_1 == True:
        if partida.ganador_1 == False:
            po = Impresion75.objects.filter(propietario__partida_id=partida.id, carton__l1_1__in=salidos,carton__l1_2__in=salidos,carton__l1_3__in=salidos,carton__l1_4__in=salidos,carton__l1_5__in=salidos) 
            if po:
                for p in po: 
                    p.ganador_1 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                partida.ganador_1=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores75.html',{'cartones':po,'figura':'Linea B'},request)
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param)

    #FIGURA 2 LINEA I
    if partida.figura_2 == True:
        if partida.ganador_2 == False:
            po = Impresion75.objects.filter(propietario__partida_id=partida.id, carton__l2_1__in=salidos,carton__l2_2__in=salidos,carton__l2_3__in=salidos,carton__l2_4__in=salidos,carton__l2_5__in=salidos,) 
            if po:
                for p in po: 
                    p.ganador_2 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                partida.ganador_2=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores75.html',{'cartones':po,'figura':'Linea I'},request)
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param)

    #FIGURA 3 LINEA N
    if partida.figura_3 == True:
        if partida.ganador_3 == False:
            po = Impresion75.objects.filter(propietario__partida_id=partida.id, carton__l3_1__in=salidos,carton__l3_2__in=salidos,carton__l3_4__in=salidos,carton__l3_5__in=salidos,) 
            if po:
                for p in po: 
                    p.ganador_3 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                partida.ganador_3=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores75.html',{'cartones':po,'figura':'Linea N'},request)
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param) 
    #FIGURA 4 LINEA G
    if partida.figura_4 == True:
        if partida.ganador_4 == False:
            po = Impresion75.objects.filter(propietario__partida_id=partida.id, carton__l4_1__in=salidos,carton__l4_2__in=salidos,carton__l4_3__in=salidos,carton__l4_4__in=salidos,carton__l4_5__in=salidos) 
            if po:
                for p in po: 
                    p.ganador_4 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                partida.ganador_4=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores75.html',{'cartones':po,'figura':'Linea G'},request)
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param) 

    #FIGURA 5 LINEA O
    if partida.figura_5 == True:
        if partida.ganador_5 == False:
            po = Impresion75.objects.filter(propietario__partida_id=partida.id, carton__l5_1__in=salidos,carton__l5_2__in=salidos,carton__l5_3__in=salidos,carton__l5_4__in=salidos,carton__l5_5__in=salidos,) 
            if po:
                for p in po: 
                    p.ganador_5 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                partida.ganador_5=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores75.html',{'cartones':po,'figura':'Linea O'},request)
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param) 

    #FIGURA 6 LA X
    if partida.figura_6 == True:
        if partida.ganador_6 == False:
            po = Impresion75.objects.filter(propietario__partida_id=partida.id, carton__l1_1__in=salidos,carton__l2_2__in=salidos,carton__l4_4__in=salidos,carton__l5_5__in=salidos,carton__l5_1__in=salidos,carton__l4_2__in=salidos,carton__l2_4__in=salidos,carton__l1_5__in=salidos)
            if po:
                for p in po: 
                    p.ganador_6 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                partida.ganador_6=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores75.html',{'cartones':po,'figura':'La X'},request)
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param) 
                

    #FIGURA 7 LA CRUZ
    if partida.figura_7 == True:
        if partida.ganador_7 == False:
            po = Impresion75.objects.filter(propietario__partida_id=partida.id, carton__l3_1__in=salidos,carton__l3_2__in=salidos,carton__l3_4__in=salidos,carton__l3_5__in=salidos,carton__l1_3__in=salidos,carton__l2_3__in=salidos,carton__l4_3__in=salidos,carton__l5_3__in=salidos,)
            if po:
                for p in po: 
                    p.ganador_7 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                partida.ganador_7=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores75.html',{'cartones':po,'figura':'La CRUZ'},request)
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param) 
                
    #FIGURA 8 LA C
    if partida.figura_8 == True:
        if partida.ganador_8 == False:
            po = Impresion75.objects.filter(propietario__partida_id=partida.id, carton__l1_1__in=salidos,carton__l1_2__in=salidos,carton__l1_3__in=salidos,carton__l1_4__in=salidos,carton__l1_5__in=salidos,carton__l5_1__in=salidos,carton__l4_1__in=salidos,carton__l3_1__in=salidos,carton__l2_1__in=salidos,carton__l5_5__in=salidos,carton__l4_5__in=salidos,carton__l3_5__in=salidos,carton__l2_5__in=salidos,)
            if po:
                for p in po: 
                    p.ganador_8 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                partida.ganador_8=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores75.html',{'cartones':po,'figura':'La C'},request)
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param) 
                
    #FIGURA 9 LA S
    if partida.figura_9 == True:
        if partida.ganador_9 == False:
            po = Impresion75.objects.filter(propietario__partida_id=partida.id, carton__l1_1__in=salidos,carton__l2_1__in=salidos,carton__l3_1__in=salidos,carton__l4_1__in=salidos,carton__l5_1__in=salidos,carton__l1_5__in=salidos,carton__l2_5__in=salidos,carton__l3_5__in=salidos,carton__l4_5__in=salidos,carton__l5_5__in=salidos,carton__l1_2__in=salidos,carton__l1_3__in=salidos,carton__l5_4__in=salidos,carton__l5_3__in=salidos,carton__l2_3__in=salidos,carton__l4_3__in=salidos,)
            if po:
                for p in po: 
                    p.ganador_9 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                partida.ganador_9=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores75.html',{'cartones':po,'figura':'La S'},request)
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param) 
    #FIGURA 10 tabla llena
    if partida.figura_10 == True:
        if partida.ganador_10 == False:
            po =Impresion75.objects.filter(
                propietario__partida_id=partida.id, 
                carton__l1_1__in=salidos,
                carton__l2_1__in=salidos,
                carton__l3_1__in=salidos,
                carton__l4_1__in=salidos,
                carton__l5_1__in=salidos,
                carton__l1_2__in=salidos,
                carton__l2_2__in=salidos,
                carton__l3_2__in=salidos,
                carton__l4_2__in=salidos,
                carton__l5_2__in=salidos,
                carton__l1_3__in=salidos,
                carton__l2_3__in=salidos,
                carton__l3_3__in=salidos,
                carton__l4_3__in=salidos,
                carton__l5_3__in=salidos,
                carton__l1_4__in=salidos,
                carton__l2_4__in=salidos,
                carton__l3_4__in=salidos,
                carton__l4_4__in=salidos,
                carton__l5_4__in=salidos,
                carton__l1_5__in=salidos,
                carton__l2_5__in=salidos,
                carton__l3_5__in=salidos,
                carton__l4_5__in=salidos,
                carton__l5_5__in=salidos,)
            if po:
                for p in po: 
                    p.ganador_10 = True
                    p.ganador = True
                    p.ganador_at = timezone.now()
                    p.save()
                partida.ganador_10=True
                partida.save()
                ganadores = render_to_string('tablero/ganadores75.html',{'cartones':po,'figura':'Tabla Llena'},request)
                param = {'ganador':ganadores,'balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
                realtime(param)
                return JsonResponse(param) 

    param = {'ganador':'none','balota':balota,'balotasJugadas':balotasJugadas,'ultimas5':ultimas5}
    realtime(param)
    return JsonResponse(param)


#loto mexicana
@login_required(login_url='/')
def Ultimas5(request,pk):
    partida = Partida.objects.get(pk=pk)
    #ULTIMAS 5 BALOTAS
    ultimas5 = Jugada.objects.filter(partida=partida).order_by('-id')[:5]
    return render(request,'tablero/ultimas5.html',{'ultimas5':ultimas5})

#bingo 75
@login_required(login_url='/')
def Ultimas575(request,pk):
    partida = Partida75.objects.get(pk=pk)
    #ULTIMAS 5 BALOTAS
    ultimas5 = Jugada75.objects.filter(partida=partida).order_by('-id')[:5]
    return render(request,'tablero/ultimas5.html',{'ultimas5':ultimas5})

def cardspartida(request,pk,dni):
    jugadas = Jugada.objects.filter(partida_id=pk)
    x = list()
    for j in jugadas:
        x.append(j.balota)
    jugadas = x
    cartones = Impresion.objects.filter(propietario__partida_id=pk, propietario__cliente__id=dni)
    return render(request,'tablero/cardsPanel.html',{'cartones':cartones,'jugadas':jugadas})

def cardspartida75(request,pk,dni):
    jugadas = Jugada75.objects.filter(partida_id=pk)
    x = list()
    for j in jugadas:
        x.append(j.balota)
    jugadas = x
    cartones = Impresion75.objects.filter(propietario__partida_id=pk, propietario__cliente__id=dni)
    return render(request,'tablero/cardsPanel75.html',{'cartones':cartones,'jugadas':jugadas})
