from django.utils import timezone
# -*- coding: utf-8 -*-
from io import BytesIO
from django.http import HttpResponse, Http404
from django.views.generic import ListView,TemplateView
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from django.contrib.auth.models import User
import time
import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count, Sum
from clientes.models import *
from cards.models import Impresion
#Workbook nos permite crear libros en excel
from openpyxl import Workbook
from partidas.models import Partida75, Partida
from cards.models import Impresion,Impresion75
class ReportePorRevendedores(TemplateView):
    template_name = "reportes-revendedores.html"
ReportePorRevendedores = ReportePorRevendedores.as_view()


def generar_pdf(request):
    if request.POST:
        desde = datetime.datetime.strptime(request.POST['desde'] + " 00:00", "%Y-%m-%d %H:%M")
        hasta = datetime.datetime.strptime(request.POST['hasta'] + " 00:00", "%Y-%m-%d %H:%M")
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "Reporte-Revendedores.pdf"  # llamado clientes
        # la linea 26 es por si deseas descargar el pdf a tu computadora
        # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
        buff = BytesIO()
        doc = SimpleDocTemplate(buff,
                                pagesize=letter,
                                rightMargin=40,
                                leftMargin=40,
                                topMargin=60,
                                bottomMargin=18,
                                )
        clientes = []
        allclientes = []
        styles = getSampleStyleSheet()
        header = Paragraph("Reporte Revendedores desde " + request.POST['desde'] + " Hasta " + request.POST['hasta'], styles['Heading1'])
        clientes.append(header)
        headings = ('Usuario', 'Tablas Vendidas', 'Monto Vendido' ,'Telefono' )

        users = User.objects.filter(is_active=True,userprofile__user_type='Revendedor')
        result = []
        for u in users:
            r = Impresion.objects.filter(propietario__fecha__range=(desde,hasta),propietario__user=u).aggregate(t=Sum('propietario__partida__monto_carton'))
            c = Impresion.objects.filter(propietario__fecha__range=(desde,hasta),propietario__user=u).count()
            a = [u.username, c, r['t'], u.userprofile.phone]
            allclientes.append(list(a))
        #allclientes = [(p.username, p.email, ) for p in User.objects.all()]

        t = Table([headings] + allclientes)
        t.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
            ]
        ))
        clientes.append(t)
        doc.build(clientes)
        response.write(buff.getvalue())
        buff.close()
        return response
    else:
        raise Http404


#FINAZAS
import re
from configuracion.models import Config

def ReporteFinanzas(request):

    desde = datetime.datetime.strptime(request.POST['desde'] + " 00:00", "%m/%d/%Y %H:%M")
    hasta = datetime.datetime.strptime(request.POST['hasta'] + " 00:00", "%m/%d/%Y %H:%M")
    if request.POST:
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "Reporte-Salas.pdf"  # llamado clientes
        # la linea 26 es por si deseas descargar el pdf a tu computadora
        # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
        buff = BytesIO()
        doc = SimpleDocTemplate(buff,
                                pagesize=letter,
                                rightMargin=40,
                                leftMargin=40,
                                topMargin=60,
                                bottomMargin=18,
                                )
        clientes = []
        allclientes = []
        styles = getSampleStyleSheet()
        header = Paragraph("Reporte Financiero Loteria Mexicana", styles['Heading1'])
        clientes.append(header)
        headings = ('Partida #', 'Vendidos','Acumulado', 'Impuesto','Total Pagado' )

        partida = Partida.objects.filter(fecha__range=(desde,hasta))
        _acumulado = 0.0
        _vendidos = 0.0
        _impuesto = 0.0
        _total = 0.0
        suma = 0
        for x in partida:
            _acumulado = _acumulado + x.monto_acumulado
            _vendidos = _vendidos + int(x.cartones_vendidos)
            _impuesto = _impuesto + x.impuesto
            _total = _total + x.total
            a = [x.pk, x.cartones_vendidos, x.monto_acumulado,x.impuesto, x.total ]
            allclientes.append(list(a))

        t = Table([headings] + allclientes)
        t.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (4, -1), 1, colors.dodgerblue),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
            ]
        ))
        clientes.append(t)
        allclientes = []
        headings = ('Total Cartones', 'Total Acumulado','Total Impuesto','Total Pagado' )
        b = [_vendidos, _acumulado, _impuesto, _total ]
        allclientes.append(list(b))
        t = Table([headings] + allclientes)
        t.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
            ]
        ))
        clientes.append(t)


        #75
        allclientes = []
        styles = getSampleStyleSheet()
        header = Paragraph("Reporte Financiero Bingo 75", styles['Heading1'])
        clientes.append(header)
        headings = ('Partida #', 'Vendidos','Acumulado', 'Impuesto','Total Pagado' )

        partida = Partida75.objects.filter(fecha__range=(desde,hasta))
        _acumulado = 0.0
        _vendidos = 0.0
        _impuesto = 0.0
        _total = 0.0
        suma = 0
        for x in partida:
            _acumulado = _acumulado + x.monto_acumulado
            _vendidos = _vendidos + int(x.cartones_vendidos)
            _impuesto = _impuesto + x.impuesto
            _total = _total + x.total
            a = [x.pk, x.cartones_vendidos, x.monto_acumulado,x.impuesto, x.total ]
            allclientes.append(list(a))

        t = Table([headings] + allclientes)
        t.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (4, -1), 1, colors.dodgerblue),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
            ]
        ))
        clientes.append(t)
        allclientes = []
        headings = ('Total Cartones', 'Total Acumulado','Total Impuesto','Total Pagado' )
        b = [_vendidos, _acumulado, _impuesto, _total ]
        allclientes.append(list(b))
        t = Table([headings] + allclientes)
        t.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
            ]
        ))
        clientes.append(t)
        doc.build(clientes)
        response.write(buff.getvalue())
        buff.close()
        return response
    else:
        raise Http404

class RepotFinanzasView(TemplateView):
    template_name = "reportFiananzas.html"

"""
class ReportSalaListView(ListView):
    model = Impresion
    template_name = "reportSalaList.html"
    desde = timezone.now()
    hasta = timezone.now()
    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        self.desde = timezone.now()
        self.hasta = timezone.now()
        return super(ReportSalaListView, self).dispatch(*args, **kwargs)
    def post(self,request,*args,**kwargs):
        self.desde = datetime.datetime.strptime(request.POST['desde'] + " 00:00", "%m/%d/%Y %H:%M")
        self.hasta = datetime.datetime.strptime(request.POST['hasta'] + " 00:00", "%m/%d/%Y %H:%M")
        return super(ReportSalaListView, self).get(request,*args, **kwargs)
    def get_queryset(self):
        sala = Sala.objects.filter(activa='Si')
        result = []
        for s in sala:
            print s.nombre
            r = Impresion.objects.filter(propietario__fecha__range=(self.desde,self.hasta),propietario__sala=s).aggregate(t=Count('propietario__sala_id'))
            g1 = Impresion.objects.filter(propietario__fecha__range=(self.desde,self.hasta),propietario__sala=s,ganador_1 = True).aggregate(t=Count('propietario__sala_id'))
            g2 = Impresion.objects.filter(propietario__fecha__range=(self.desde,self.hasta),propietario__sala=s,ganador_2 = True).aggregate(t=Count('propietario__sala_id'))
            g3 = Impresion.objects.filter(propietario__fecha__range=(self.desde,self.hasta),propietario__sala=s,ganador_3 = True).aggregate(t=Count('propietario__sala_id'))
            g4 = Impresion.objects.filter(propietario__fecha__range=(self.desde,self.hasta),propietario__sala=s,ganador_4 = True).aggregate(t=Count('propietario__sala_id'))
            g5 = Impresion.objects.filter(propietario__fecha__range=(self.desde,self.hasta),propietario__sala=s,ganador_5 = True).aggregate(t=Count('propietario__sala_id'))
            g6 = Impresion.objects.filter(propietario__fecha__range=(self.desde,self.hasta),propietario__sala=s,ganador_6 = True).aggregate(t=Count('propietario__sala_id'))
            g7 = Impresion.objects.filter(propietario__fecha__range=(self.desde,self.hasta),propietario__sala=s,ganador_7 = True).aggregate(t=Count('propietario__sala_id'))
            ganadores = g1['t'] + g2['t'] + g3['t'] + g4['t'] + g5['t'] + g6['t'] + g7['t'] 
            a = {'nombre': s.nombre, 'vendidos': r['t'], 'ganadores':ganadores}
            result.append(dict(a))
            print result
        return result
    def desde(self):
        return self.desde
    def hasta(self):
        return self.hasta



def generar_pdf(request):
    print "Genero el PDF"
    desde = datetime.datetime.strptime(request.POST['desde'] + " 00:00", "%m/%d/%Y %H:%M")
    hasta = datetime.datetime.strptime(request.POST['hasta'] + " 00:00", "%m/%d/%Y %H:%M")
    if request.POST:
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "Reporte-Salas.pdf"  # llamado clientes
        # la linea 26 es por si deseas descargar el pdf a tu computadora
        # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
        buff = BytesIO()
        doc = SimpleDocTemplate(buff,
                                pagesize=letter,
                                rightMargin=40,
                                leftMargin=40,
                                topMargin=60,
                                bottomMargin=18,
                                )
        clientes = []
        allclientes = []
        styles = getSampleStyleSheet()
        header = Paragraph("Reporte Por Salas", styles['Heading1'])
        clientes.append(header)
        headings = ('Sala', 'Vendidos', 'Ganadores' )

        sala = Sala.objects.filter(activa='Si')
        result = []
        for s in sala:
            r = Impresion.objects.filter(propietario__fecha__range=(desde,hasta),propietario__sala=s).aggregate(t=Count('propietario__sala_id'))
            g1 = Impresion.objects.filter(propietario__fecha__range=(desde,hasta),propietario__sala=s,ganador_1 = True).aggregate(t=Count('propietario__sala_id'))
            g2 = Impresion.objects.filter(propietario__fecha__range=(desde,hasta),propietario__sala=s,ganador_2 = True).aggregate(t=Count('propietario__sala_id'))
            g3 = Impresion.objects.filter(propietario__fecha__range=(desde,hasta),propietario__sala=s,ganador_3 = True).aggregate(t=Count('propietario__sala_id'))
            g4 = Impresion.objects.filter(propietario__fecha__range=(desde,hasta),propietario__sala=s,ganador_4 = True).aggregate(t=Count('propietario__sala_id'))
            g5 = Impresion.objects.filter(propietario__fecha__range=(desde,hasta),propietario__sala=s,ganador_5 = True).aggregate(t=Count('propietario__sala_id'))
            g6 = Impresion.objects.filter(propietario__fecha__range=(desde,hasta),propietario__sala=s,ganador_6 = True).aggregate(t=Count('propietario__sala_id'))
            g7 = Impresion.objects.filter(propietario__fecha__range=(desde,hasta),propietario__sala=s,ganador_7 = True).aggregate(t=Count('propietario__sala_id'))
            g8 = Impresion.objects.filter(propietario__fecha__range=(desde,hasta),propietario__sala=s,ganador_8 = True).aggregate(t=Count('propietario__sala_id'))
            g9 = Impresion.objects.filter(propietario__fecha__range=(desde,hasta),propietario__sala=s,ganador_9 = True).aggregate(t=Count('propietario__sala_id'))
            g10 = Impresion.objects.filter(propietario__fecha__range=(desde,hasta),propietario__sala=s,ganador_10 = True).aggregate(t=Count('propietario__sala_id'))
            ganadores = g1['t'] + g2['t'] + g3['t'] + g4['t'] + g5['t'] + g6['t'] + g7['t']  + g8['t']  + g9['t']  + g10['t'] 
            # a = ['nombre': s.nombre, 'vendidos': r['t'], 'ganadores':ganadores]
            a = [s.nombre, r['t'], ganadores]
            allclientes.append(list(a))
        #allclientes = [(p.username, p.email, ) for p in User.objects.all()]

        t = Table([headings] + allclientes)
        t.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
            ]
        ))
        clientes.append(t)
        doc.build(clientes)
        response.write(buff.getvalue())
        buff.close()
        return response
    else:
        raise Http404



def ReportePCartones(request,id):
    print "Genero el PDF"
    partida = id
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Reporte-Partidas.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    clientes = []
    allclientes = []
    styles = getSampleStyleSheet()
    header = Paragraph("Reporte de Cartones Partida Nº: " + str(partida), styles['Heading1'])
    clientes.append(header)
    headings = ('ID Carton', 'Premio', 'Fecha/Hora','Sala' )

    cartones = Impresion.objects.filter(propietario__partida_id=partida, ganador=True)
    for c in cartones:
        premio = ""
        if c.ganador_1 is True:
            premio = "Primera Linea"
        elif c.ganador_2 is True:
            premio = "Primera y Segunda Linea"
        elif c.ganador_3 is True:
            premio = "Primera y Tercera Linea"
        elif c.ganador_4 is True:
            premio = "Segunda Linea"
        elif c.ganador_5 is True:
            premio = "Segunda y Tercera Linea"
        elif c.ganador_6 is True:
            premio = "Tercera Linea"
        elif c.ganador_7 is True:
            premio = "Bingo"
        elif c.ganador_8 is True:
            premio = "Linea al Azar"
        elif c.ganador_9 is True:
            premio = "ReBingo"
        elif c.ganador_10 is True:
            premio = "Revancha"
         # a = ['nombre': s.nombre, 'vendidos': r['t'], 'ganadores':ganadores]
        a = [c.id, premio, c.ganador_at,c.propietario.sala.nombre]
        allclientes.append(list(a))
    #allclientes = [(p.username, p.email, ) for p in User.objects.all()]
    t = Table([headings] + allclientes)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    clientes.append(t)
    doc.build(clientes)
    response.write(buff.getvalue())
    buff.close()
    return response


def ReportePartida(request,id):
    print "Genero el PDF"
    partida = id
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Reporte-Partidas.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    clientes = []
    allclientes = []
    styles = getSampleStyleSheet()
    header = Paragraph("Reporte de Partida Nº: " + str(partida), styles['Heading1'])
    clientes.append(header)
    headings = ('Salida','Balota', 'Fecha/Hora',)

    balotas = Jugada.objects.filter(partida_id=partida,).order_by('id')
    i = 0
    for b in balotas:
        i = i + 1
         # a = ['nombre': s.nombre, 'vendidos': r['t'], 'ganadores':ganadores]
        a = [i, b.balota, b.created_at]
        allclientes.append(list(a))
    #allclientes = [(p.username, p.email, ) for p in User.objects.all()]
    t = Table([headings] + allclientes)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    clientes.append(t)
    doc.build(clientes)
    response.write(buff.getvalue())
    buff.close()
    return response

#Nuestra clase hereda de la vista genérica TemplateView
class ReportePartidasExcel(TemplateView):
     
    #Usamos el método get para generar el archivo excel 
    def get(self, request, *args, **kwargs):
        #Obtenemos todas las personas de nuestra base de datos
        personas = Cliente.objects.all()
        #Creamos el libro de trabajo
        wb = Workbook()
        #Definimos como nuestra hoja de trabajo, la hoja activa, por defecto la primera del libro
        ws = wb.active
        #En la celda B1 ponemos el texto 'REPORTE DE PERSONAS'
        # ws['B1'] = 'REPORTE DE PERSONAS'
        # #Juntamos las celdas desde la B1 hasta la E1, formando una sola celda
        # ws.merge_cells('B1:E1')
        # #Creamos los encabezados desde la celda B3 hasta la E3
        ws['A1'] = 'P. ID'
        ws['B1'] = 'P. Descripcion'
        ws['C1'] = 'S. ID'
        ws['D1'] = 'S. Nombre'       
        ws['E1'] = 'Asignacion'       
        cont=2
        
        dt = datetime.datetime.strptime(request.GET['v'] + " 00:00", "%m/%d/%Y %H:%M")
        #Recorremos el conjunto de las Partidas por la fecha parametro del get
        partidas = Partida.objects.filter(fecha = dt);
        for partida in partidas:
            for sala in Sala.objects.filter(activa='Si'):
                ws.cell(row=cont,column=1).value = partida.id
                ws.cell(row=cont,column=2).value = partida.descripcion
                ws.cell(row=cont,column=3).value = sala.id
                ws.cell(row=cont,column=4).value = sala.nombre  
                ws.cell(row=cont,column=5).value = 0
                cont = cont + 1
        # #Establecemos el nombre del archivo
        nombre_archivo = "Asignar.xlsx"
        #Definimos que el tipo de respuesta a devolver es un archivo de microsoft excel
        response = HttpResponse(content_type="application/ms-excel") 
        contenido = "attachment; filename={0}".format(nombre_archivo)
        response["Content-Disposition"] = contenido
        wb.save(response)
        return response




#Nuestra clase hereda de la vista genérica TemplateView
class MoeloPartida(TemplateView):
     
    #Usamos el método get para generar el archivo excel 
    def get(self, request, *args, **kwargs):
        #Obtenemos todas las personas de nuestra base de datos
        personas = Cliente.objects.all()
        #Creamos el libro de trabajo
        wb = Workbook()
        #Definimos como nuestra hoja de trabajo, la hoja activa, por defecto la primera del libro
        ws = wb.active
        #En la celda B1 ponemos el texto 'REPORTE DE PERSONAS'
        # ws['B1'] = 'REPORTE DE PERSONAS'
        # #Juntamos las celdas desde la B1 hasta la E1, formando una sola celda
        # ws.merge_cells('B1:E1')
        # #Creamos los encabezados desde la celda B3 hasta la E3
        ws['A1'] = 'Fecha'
        ws['B1'] = 'Descripcion'
        ws['C1'] = 'L1'
        ws['D1'] = 'MONTOL1'
        ws['E1'] = 'L1-L2'
        ws['F1'] = 'MONTOL1L2'
        ws['G1'] = 'L1-L3'       
        ws['H1'] = 'MONTOL1L3'       
        ws['I1'] = 'L2'       
        ws['J1'] = 'MONTOL2'       
        ws['K1'] = 'L2-L3'       
        ws['L1'] = 'MONTOL2L3'       
        ws['M1'] = 'L3'       
        ws['N1'] = 'MONTOL3'       
        ws['O1'] = 'BINGO'       
        ws['P1'] = 'MONTOBINGO'       
        ws['Q1'] = 'LA'       
        ws['R1'] = 'MONTOLA'       
        ws['S1'] = 'REVANCHA'       
        ws['T1'] = 'MONTOREVANCHA'       
        ws['U1'] = 'REBINGO'       
        ws['V1'] = 'MONTOREBINGO'       
        ws['W1'] = 'VALORCARTON'       
        # #Establecemos el nombre del archivo
        nombre_archivo = "FormatoPartidas.xlsx"
        #Definimos que el tipo de respuesta a devolver es un archivo de microsoft excel
        response = HttpResponse(content_type="application/ms-excel") 
        contenido = "attachment; filename={0}".format(nombre_archivo)
        response["Content-Disposition"] = contenido
        wb.save(response)
        return response
"""
