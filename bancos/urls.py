from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import BancoList, BancoCreate, BancoDelete, BancoUpdate, Comprar, BancoView, pagarcompra, \
comprasprocesos, deleteCompras, verCompra, aprobarCompra, Comprar75,pagarcompra75, comprasprocesos75, verCompra75, \
aprobarCompra75, pagarcomprapaypal, pagarcomprapaypal75

urlpatterns = ([
    path('', login_required(BancoList), name='list-banco'),   
    path('crear/', login_required(BancoCreate), name='crear-banco'),    
    path('delete-banco/<int:pk>/', login_required(BancoDelete), name='delete-banco'),
    path('update/<int:pk>/', login_required(BancoUpdate), name='update-banco'),    
    path('comprar/<int:pk>/', login_required(Comprar), name='comprar'),    
    path('75/comprar/<int:pk>/', login_required(Comprar75), name='comprar75'),    
    path('banco-view', login_required(BancoView), name='banco-view'),    
    path('pagar/<int:pk>/', login_required(pagarcompra), name='pagar'),    
    path('75/pagar/<int:pk>/', login_required(pagarcompra75), name='pagar75'),    
    path('compras-pendientes', login_required(comprasprocesos), name='compras'),    
    path('75/compras-pendientes', login_required(comprasprocesos75), name='compras75'),    
    path('delete-compra/<int:pk>/', login_required(deleteCompras), name='delete-compras'),    
    path('ver-compra/<int:pk>/', login_required(verCompra), name='ver-compra'),    
    path('75/ver-compra/<int:pk>/', login_required(verCompra75), name='ver-compra75'),    
    path('aprovar-compra/<int:pk>/', login_required(aprobarCompra), name='aprobar-compra'),    
    path('75/aprovar-compra/<int:pk>/', login_required(aprobarCompra75), name='aprobar-compra75'),    
    path('pagar-paypal/<int:pk>/', login_required(pagarcomprapaypal), name='pagar-paypal'),    
    path('75/pagar-paypal/<int:pk>/', login_required(pagarcomprapaypal75), name='pagar-paypal75'),    
    ])

