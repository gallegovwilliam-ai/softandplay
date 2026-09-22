from django.urls import re_path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    re_path(r'^revendedores/$',login_required(ReportePorRevendedores) , name="reporte-revendedores" ),
    re_path(r'^generar-revendedores/$',login_required(generar_pdf) , name="generar-revendedores" ),
    re_path(r'^finanzas/$', RepotFinanzasView.as_view(), name="finanzasR" ),
    re_path(r'^finanzas-total/$', ReporteFinanzas, name="finanzas-total" ),
]