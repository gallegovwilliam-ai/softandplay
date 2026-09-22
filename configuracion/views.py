from django.shortcuts import render, redirect, HttpResponse, Http404
from django.urls import  reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView 
import  datetime
from configuracion.models import Config
# Create your views here.

class Configuracion(UpdateView):
    model = Config
    success_url = reverse_lazy('config',kwargs={'pk': 1})
    template_name = "config.html"
    fields = [
        'titulo',
        'logo',
        'logo_horizontal',
        'fondo_login_desktop',
        'fondo_login_mobile',
        'fondo_pantalla_mexicana',
        'fondo_pantalla_bingo',
        'fondo_carton_bingo',
        'fondo_carton_lotoMX',
        'tapa_balota_bingo',
        'tapa_carta_lotoMX',
        'impuesto'
    ]
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
    
Configuracion = Configuracion.as_view()