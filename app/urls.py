"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth import views as auth_views
from django.urls import  reverse_lazy
from core.views import home, Notify_test
from user_profile.views import login

def handler404(request, exception, template_name="404.html"):
    response = render(request,"404.html")
    response.status_code = 404
    return response

def handler500(request, template_name="500.html"):
    response = render(request,"500.html")
    response.status_code = 500
    return response

urlpatterns = [
    path('api-v01/', include('api.urls'), name="api",),
    path('config/', include('configuracion.urls'), name="configuracion",),
    path('pagos/', include('pagos.urls'), name="pagos",),
    path('account/', include('user_profile.urls'), name="users",),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('reporte/', include('reportes.urls'), name="reportes"),
    path('messages/', include('usermessages.urls'), name="usermessages"),
    path('clientes/', include('clientes.urls'), name="usermessages"),
    path('bancos/', include('bancos.urls'), name="bancos"),
    path('chance/', include('chance.urls'), name="chance"),
    path('partidas/', include('partidas.urls'), name="partidas"),
    path('cartones/', include('cards.urls'), name="cartones"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("login/", login, name="login"),
    #path('admin/', admin.site.urls),
    path('',home),
    path('test-notify',Notify_test, name="tf")
]
