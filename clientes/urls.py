from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import ClienteList, ClienteCreate, ClienteDelete,ClienteUpdate, VerificarCliente
urlpatterns = ([
    path('', login_required(ClienteList), name='list-cliente'),    
    path('crear/', login_required(ClienteCreate), name='crear-cliente'),    
    path('verificar/', login_required(VerificarCliente), name='verificar-cliente'),    
    path('delete/<int:pk>/', login_required(ClienteDelete), name='delete-cliente'),
    path('update/<int:pk>/', login_required(ClienteUpdate), name='update-cliente'),    
    ])

