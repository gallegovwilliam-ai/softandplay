# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import Partida, Partida75
from core.forms import BaseForm
DATE_INPUT_FORMATS = ['%d-%m-%Y']

class PartidaForm(ModelForm):
	fecha = forms.DateField(label="Fecha",widget=forms.DateInput(format='%Y-%m-%d',attrs={'type':'date','class': 'form-control','placeholder':'Ingrese la Fecha'}),input_formats=DATE_INPUT_FORMATS,required=False,) 
	descripcion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Descripción'}),label="Descripción",required=False) 	
	figura_1 = forms.BooleanField(label="Linea al Azar (verticales y horizontales)",required=False)
	porciento_1 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje Linea al Azar'}),label="",required=False) 	
	figura_2 = forms.BooleanField(label="Primera Linea Vertical",required=False)
	porciento_2 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje Primera Linea Vertical'}),label="",required=False) 	
	figura_3 = forms.BooleanField(label="Segunda Linea Vertical",required=False)
	porciento_3 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje Segunda Linea Vertical'}),label="",required=False) 	
	figura_4 = forms.BooleanField(label="Tercera Linea Vertical",required=False)
	porciento_4 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje Tercera Linea Vertical'}),label="",required=False) 	
	figura_5 = forms.BooleanField(label="Cuarta Linea Vertical",required=False)
	porciento_5 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje Cuarta Linea Vertical'}),label="",required=False) 	
	figura_6 = forms.BooleanField(label="Primera Linea horizontal",required=False)
	porciento_6 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje Primera Linea horizontal'}),label="",required=False) 	
	figura_7 = forms.BooleanField(label="Segunda Linea horizontal",required=False)
	porciento_7 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje Segunda Linea horizontal'}),label="",required=False) 	
	figura_8 = forms.BooleanField(label="Tercera Linea horizontal",required=False)
	porciento_8 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje Tercera Linea horizontal'}),label="",required=False) 	
	figura_9 = forms.BooleanField(label="Cuarta  Linea horizontal",required=False)
	porciento_9 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje Cuarta  Linea horizontal'}),label="",required=False) 	
	figura_10 = forms.BooleanField(label="Tabla Llena",required=False)
	porciento_10 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje Tabla Llena'}),label="",required=False) 	
	monto_carton = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Precio Tabla'}),label="Valor tabla",required=False) 
	class Meta:
		model = Partida
		fields = (
			'fecha',
		    'descripcion',
		    'figura_1',
		    'porciento_1',
		    'figura_2',
		    'porciento_2',
		    'figura_3',
		    'porciento_3',
		    'figura_4',
		    'porciento_4', 
		    'figura_5',
		    'porciento_5',
		    'figura_6',
		    'porciento_6',
		    'figura_7',
		    'porciento_7',
		    'figura_8',
		    'porciento_8',
		    'figura_9',
		    'porciento_9',
		    'figura_10',
		    'porciento_10',
		    'monto_carton',			
		)


class Partida75Form(ModelForm):
	fecha = forms.DateField(label="Fecha",widget=forms.DateInput(format='%Y-%m-%d',attrs={'type':'date','class': 'form-control','placeholder':'Ingrese la Fecha'}),input_formats=DATE_INPUT_FORMATS,required=False,) 
	descripcion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Descripción'}),label="Descripción",required=False) 	
	figura_1 = forms.BooleanField(label="Linea B",required=False)
	porciento_1 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje Linea B'}),label="",required=False) 	
	figura_2 = forms.BooleanField(label="Linea I",required=False)
	porciento_2 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje Linea I'}),label="",required=False) 	
	figura_3 = forms.BooleanField(label="Linea N",required=False)
	porciento_3 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje Linea N'}),label="",required=False) 	
	figura_4 = forms.BooleanField(label="Linea G",required=False)
	porciento_4 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje Linea G'}),label="",required=False) 	
	figura_5 = forms.BooleanField(label="Linea O",required=False)
	porciento_5 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje Linea O'}),label="",required=False) 	
	figura_6 = forms.BooleanField(label="La X",required=False)
	porciento_6 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje de la X'}),label="",required=False) 	
	figura_7 = forms.BooleanField(label="La Cruz",required=False)
	porciento_7 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje de la Cruz'}),label="",required=False) 	
	figura_8 = forms.BooleanField(label="La C",required=False)
	porciento_8 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje de la C'}),label="",required=False) 	
	figura_9 = forms.BooleanField(label="La S",required=False)
	porciento_9 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje de la S'}),label="",required=False) 	
	figura_10 = forms.BooleanField(label="Tabla Llena",required=False)
	porciento_10 = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Porcentaje Tabla Llena'}),label="",required=False) 	
	monto_carton = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control numeric','type':'number','placeholder':'Precio Tabla'}),label="Valor tabla",required=False) 
	class Meta:
		model = Partida75
		fields = (
			'fecha',
		    'descripcion',
		    'figura_1',
		    'porciento_1',
		    'figura_2',
		    'porciento_2',
		    'figura_3',
		    'porciento_3',
		    'figura_4',
		    'porciento_4', 
		    'figura_5',
		    'porciento_5',
		    'figura_6',
		    'porciento_6',
		    'figura_7',
		    'porciento_7',
		    'figura_8',
		    'porciento_8',
		    'figura_9',
		    'porciento_9',
		    'figura_10',
		    'porciento_10',
		    'monto_carton',			
		)
	   	   