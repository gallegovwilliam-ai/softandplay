from django.urls import path
from .views import Configuracion
from rest_framework.authtoken import views
from django.contrib.auth.decorators import login_required

urlpatterns = ([
    path('<int:pk>/', login_required(Configuracion),  name='config'),    
    ])

