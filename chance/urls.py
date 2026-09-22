from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import LotoChanceCreateView, LotoChanceList, LotoChanceUpdateView, LotoChanceDelete, VentaRevendedor, \
    AsignarNumero, EliminarNumero, RealizarVentar
    

urlpatterns = ([
    path('', login_required(LotoChanceList), name='list-chance'),   
    path('crear/', login_required(LotoChanceCreateView), name='crear-chance'),    
    path('update/<int:pk>/', login_required(LotoChanceUpdateView), name='update-chance'),    
    path('delete/<int:pk>/', login_required(LotoChanceDelete), name='delete-chance'),
    path('delete-numero/<int:pk>/', login_required(EliminarNumero), name='delete-numero'),
    path('vender/', login_required(VentaRevendedor), name='vender-chance'),    
    path('asignar-numero/', login_required(AsignarNumero), name='asignar-numero'),    
    path('realizar-venta/', login_required(RealizarVentar), name='realizar-venta'),    
    ])

