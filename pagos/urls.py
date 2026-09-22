from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import PagosList, CartonGanador, Mensaje, Mensaje75, MisGanadores,ProcesarPagoCarton, CartonGanador75, ProcesarPagoCarton75
urlpatterns = ([
    path('mis-ganadores/', login_required(MisGanadores), name='mis-ganadores'),    
    path('pendientes/', login_required(PagosList), name='pagos-pendientes'),    
    path('ver-carton/<int:pk>/', login_required(CartonGanador), name='ver-carton-ganador'),    
    path('75/ver-carton/<int:pk>/', login_required(CartonGanador75), name='ver-carton-ganador75'),    
    path('mensaje/<int:pk>/', login_required(Mensaje), name='mensaje-carton'),    
    path('75/mensaje/<int:pk>/', login_required(Mensaje75), name='mensaje-carton75'),    
    path('procesar/<int:pk>/', login_required(ProcesarPagoCarton), name='procesar-pago'),    
    path('75/procesar/<int:pk>/', login_required(ProcesarPagoCarton75), name='procesar-pago75'),    
     ])

