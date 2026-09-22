from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import Inprimir, Inprimir75, tikect, tikect75, xls, xls75
urlpatterns = ([
    path('xls/<int:nee>/', login_required(xls), name='xls'),       
    path('75/xls/<int:nee>/', login_required(xls75), name='xls75'),       
    path('vender/', login_required(Inprimir), name='vender'),       
    path('tikect/', login_required(tikect), name='tikect'),       
    path('75/vender/', login_required(Inprimir75), name='vender75'),       
    path('75/tikect/', login_required(tikect75), name='tikect75'),       
    ])

