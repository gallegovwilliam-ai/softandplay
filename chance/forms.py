# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import LotoChance
from core.forms import BaseForm

class LotoChanceForm(BaseForm):
	class Meta:
		model = LotoChance
		fields = (
			'nombre',
			'thumb',
			)
