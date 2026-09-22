# -*- encoding: utf-8 -*-
from django import forms
from .models import Banco
from core.forms import BaseForm

class BancoForm(BaseForm):
	class Meta:
		model = Banco
		fields = (
			'moneda',
			'corresponsal',
		    'ciudad',
		    'codigo_swift',
		    'banco_benef',
		    'cuenta',
		    'beneficiario_final',
		    'cuenta_abono',
		)
  