# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import Cliente
from core.forms import BaseForm

class ClienteForm(BaseForm):
	class Meta:
		model = Cliente
		fields = (
			'nombre',
			'apellido',
			'dni',
			'direccion',
			'telefono',
			'email',
			)
