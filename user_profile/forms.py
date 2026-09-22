# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from user_profile.models import UserProfile

USER_TYPE = [
		('Revendedor','Revendedor'), 
		('Usuario','Usuario'), 
	]
BLOCK_TYPE = [
		('si','si'),
		('no','no')
]
class BaseForm(ModelForm):
    def __init__(self, request,*args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
        	field.widget.attrs['class'] = 'form-control'

class RegisterUserForm(BaseForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email',]
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({'required':'','readonly':''})


class RegisterUserProfileForm(BaseForm):
	user_type = forms.CharField(widget=forms.Select(choices=USER_TYPE,))	
	block = forms.CharField(widget=forms.Select(choices=BLOCK_TYPE,))	
	class Meta:
		model = UserProfile
		fields = ['country', 'state','city', 'phone', 'address','user_type','block','thumb']
	
class ChangeNameForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control round-input'}),label="Nombre", required=True,error_messages={'required': 'Debe ingresar el Nombre.'}) 
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control round-input'}),label="Apellido", required=True,error_messages={'required': 'Debe ingresar el Apellido.'})
    class Meta:
        model = User
        fields = ('first_name', 'last_name' )

class ChangeEmailForm(ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control round-input'}),required=True,error_messages={'required': 'Debe ingresar un Email.','valid':'valido'})
    class Meta:
        model = User
        fields = ('email',)