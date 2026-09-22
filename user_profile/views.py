# -*- encoding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import  PasswordChangeForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.models import User as SolicitudUser
from user_profile.models import UserProfile
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse, reverse_lazy
from configuracion.models import Config
#CONTAR REGISTROS
#from django.db.models import Co
#co =  User.objects.annotate(cont = Count('pk'))
#print co[0].cont


from random import choice

longitud = 6
valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<=>@#%&+"

from .forms import *

import re
def login(request):
    MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)", re.IGNORECASE)
    is_mobile = True if MOBILE_AGENT_RE.match(request.META.get('HTTP_USER_AGENT', '')) else False    
    if request.method == 'GET':
        if request.user.pk:
            return  redirect('/')
        if not is_mobile:
            return render(request, 'login.html')
        else:
            return render(request, 'login.html')
        
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.userprofile.block == 'no':
                auth_login(request, user,backend='django.contrib.auth.backends.ModelBackend')
                return HttpResponse('ok')
            else:
                return HttpResponse('block')
        else:
            return HttpResponse('passwordError')
    else:
        raise Http404
#340 215
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
def SendMail(template,user,titulo, context=None):
    data = {'user': user}
    if context:
        data.update(context)
    body = render_to_string(template, data)
    email = EmailMessage(
        subject=titulo,
        body=body,
        from_email='No Reply<contacto@multibingos.net>',
        to=[user.email],
    )
    email.content_subtype = 'html'
    email.send()


def solicitar_validacion(request):
    if request.method != 'POST' or not request.user.is_authenticated:
        return HttpResponse(status=405)
    token = default_token_generator.make_token(request.user)
    uidb64 = urlsafe_base64_encode(str(request.user.pk).encode())
    validation_url = request.build_absolute_uri(reverse('validar_email', kwargs={'uidb64': uidb64, 'token': token}))
    try:
        SendMail('validar_email.html', request.user, 'Validación de email', {'validation_url': validation_url})
    except Exception:
        return HttpResponse('No fue posible enviar el correo de validación', status=503)
    return HttpResponse('ok')


def validar_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        raise Http404

    if not default_token_generator.check_token(user, token):
        return HttpResponse('Enlace de validación inválido o vencido', status=400)

    profile = UserProfile.objects.get(user=user)
    profile.validado = True
    profile.save(update_fields=['validado'])
    return redirect('/')



def RegisterForm(request):
    MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)", re.IGNORECASE)
    is_mobile = True if MOBILE_AGENT_RE.match(request.META.get('HTTP_USER_AGENT', '')) else False    
    if request.method == 'GET':
        if not is_mobile:
            return render(request,'singup.html',)
        else:
            return render(request,'singup.html')

    if request.method == 'POST':
        try:
            User.objects.get(username=request.POST.get('username'))
            return HttpResponse('errorUsername')
        except ObjectDoesNotExist:
            try:
                User.objects.get(email=request.POST.get('email'))
                return HttpResponse('errorEmail')
            except ObjectDoesNotExist:
                user_created=User.objects.create(first_name=request.POST['nombre'], username=request.POST['username'], email=request.POST['email'],password=make_password(request.POST.get('password')))
                user_created.save()
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')        
                try:
                    op = dict(getUserCountry(ip))
                    pais = op.get('country', 'N/A')
                except Exception:
                    pais = 'N/A'
                UserProfile.objects.create(user=user_created,country=pais,phone=request.POST['telefono'],registered=True,validado=False)
                auth_login(request, user_created,backend='django.contrib.auth.backends.ModelBackend')
                token = default_token_generator.make_token(user_created)
                uidb64 = urlsafe_base64_encode(str(user_created.pk).encode())
                validation_url = request.build_absolute_uri(reverse('validar_email', kwargs={'uidb64': uidb64, 'token': token}))
                try:
                    SendMail('validar_email.html', user_created, 'Validación de email', {'validation_url': validation_url})
                except Exception:
                    pass
                return HttpResponse('ok')
    else:
        raise Http404


import requests
import json
def getUserCountry(ip):
    # URL de la API
    api_url = "http://ip-api.com/json/"
    # Definimos los parametros de respuesta que queremos obtener
    parametros = 'status,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query'
    data = {"fields":parametros}
    # Nos conectamos con la API
    res = requests.get(api_url+ip, data=data, timeout=3)
    res.raise_for_status()
    # Obtenemos y procesamos la respuesta JSON
    api_json_res = json.loads(res.content)
    return api_json_res


@login_required
def CompleteRegistre(request):
    if request.user.userprofile.registered:
        return redirect('/')
    user_form = RegisterUserForm(data=request.POST or None,request=request,instance=request.user)
    user_profile_form = RegisterUserProfileForm(data=request.POST or None,files=request.FILES or None,request=request,instance=request.user.userprofile)

    if request.method == 'GET':
        return render(request, 'complete_register.html',{"Uform": user_form,'Pform': user_profile_form})
    else:
        user_form.save()
        profile = UserProfile.objects.get(user=request.user)
        profile.country = request.POST['country']
        profile.city = request.POST['city']
        profile.state = request.POST['state']
        profile.address = request.POST['address']
        profile.phone = request.POST['phone']
        requested_type = request.POST.get('user_type', 'Usuario')
        if requested_type not in ('Usuario', 'Revendedor'):
            requested_type = 'Usuario'
        profile.user_type = requested_type
        if requested_type=='Revendedor':
            User.objects.filter(pk=request.user.pk).update(is_staff=True)
            profile.block='si'
        profile.registered = True
        profile.save()
        #UserProfile.objects.filter(user=request.user).update(registered=True)
        SendMail('complete_email.html',request.user,'multibingos.net registro en proceso')
        if requested_type=='Revendedor':
            return redirect(reverse_lazy('logout'))
        return redirect('/')
    return True



class UsersList(ListView):
    model = User
    template_name = 'list_users.html'
    def get_queryset(self,*args,**kwargs):
        if not self.request.user.is_superuser:
            raise Http404
        return User.objects.filter(is_active=True,userprofile__block='no')
UsersList = UsersList.as_view()

class PendientesList(ListView):
    model = User
    template_name = 'list_pendiente.html'
    def get_queryset(self,*args,**kwargs):
        if not self.request.user.is_superuser:
            raise Http404
        return User.objects.filter(is_active=True,userprofile__block='si')
PendientesList = PendientesList.as_view()


@login_required
def UserUpdate(request,pk):
    if not request.user.is_superuser:
        raise Http404
    if request.method == 'GET':
        user = User.objects.get(pk = pk)
        userprofile = UserProfile.objects.get(user=user)
        user_form = RegisterUserForm(data=request.POST or None,request=request,instance=user)
        user_profile_form = RegisterUserProfileForm(data=request.POST or None,files=request.FILES or None,request=request,instance=userprofile)
        return render(request,'update_user.html', {'uform':user_form,'pform':user_profile_form,'pk':user.pk})

    elif request.method == 'POST':
        user = User.objects.get(pk = pk)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        profile = UserProfile.objects.get(user=user)
        profile.country = request.POST['country']
        profile.city = request.POST['city']
        profile.state = request.POST['state']
        profile.address = request.POST['address']
        profile.phone = request.POST['phone']
        requested_type = request.POST.get('user_type', 'Usuario')
        if requested_type not in ('Usuario', 'Revendedor'):
            raise Http404
        profile.user_type = requested_type
        if not user.is_superuser:
            user.is_staff = (requested_type == 'Revendedor')
            user.save(update_fields=['is_staff'])
        profile.registered = True
        try:
            profile.thumb = request.FILES['thumb']
        except MultiValueDictKeyError:
            pass
        profile.save()
    return redirect(reverse_lazy('users-list'))       


@login_required
def UserDelete(request,pk):
    if not request.user.is_superuser:
        raise Http404
    if request.method != 'POST':
        return HttpResponse(status=405)
    user = User.objects.filter(pk=pk).first()
    if not user:
        raise Http404
    user.is_active = False
    user.save(update_fields=['is_active'])
    UserProfile.objects.filter(user=user).update(active=False)
    return redirect(reverse_lazy('users-list'))


class Solicitud(DetailView):
    model = UserProfile
    template_name = 'solicitud.html'
    def dispatch(self,*args, **kwargs):
        if self.request.user.is_superuser:
            return super().dispatch( *args, **kwargs)
        else:
            raise Http404
    def get_queryset(self):
        return UserProfile.objects.filter(user_id=self.kwargs['pk'])
Solicitud = Solicitud.as_view()

def Aprobar(request,pk):
    if request.user.is_superuser:
        u = UserProfile.objects.get(pk=pk)
        u.block = 'no'
        u.save()
        SendMail('aprobado_email.html',u.user,'Bienvenido a multibingos.net')        
        return redirect(reverse_lazy('pendiente-list'))
    else:
        raise Http404
    return 1

"""
class IndexView(TemplateView):
    template_name='login.html'



class UsuarioCreateView(CreateView):
    form_class = UsuarioForm
    template_name = "crearUsuario.html"
    success_url="/usuario/"
    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(UsuarioCreateView, self).dispatch(*args, **kwargs)
    def post(self,request, *args, **kwargs):
        try:
            usuario = User.objects.get(email=request.POST['email'])
            return HttpResponse('existeEmail')
        except ObjectDoesNotExist:
            pass
        try:
            usuario = User.objects.get(username=request.POST['username'])
            return HttpResponse('existeUser')
        except ObjectDoesNotExist:
            usuario = User.objects.create(username=request.POST['username'],first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'])
            try:            
                s = Sala.objects.get(pk=request.POST['sala'])                
                profile  = UserProfile.objects.create(user_id=usuario.id,sala=s,telefono=request.POST['telefono'],thumb=request.FILES['file'])            
            except MultiValueDictKeyError:
                profile  = UserProfile.objects.create(user_id=usuario.id,sala=s,telefono=request.POST['telefono'])            

            p = "123456"
            # p = p.join([choice(valores) for i in range(longitud)])
            usuario.password = make_password(p)    
            usuario.save()
            # titulo = 'Usuario Creado'
            # msj = 'Saludos Gracias por utilizar los servicios de ' + settings.SITIO + ', Su Usuario:' + usuario.username + ' clave: ' + p + '  El equipo de ' + settings.SITIO + ' Gracias' 
            # html = '<table style="width:600px;margin:auto"><tr> <td style="background:#eeeeee"><p style="width:80%;margin:auto;padding:20px;font-size:1.5em;"> <b>Saludos</b><br> Gracias por utilizar los servicios de <a href="http://' + settings.SITIO + '">' + settings.SITIO + '</a>:<br><b>Usuario:</b> ' + usuario.username + '<br><b>Clave:</b> ' + p + '<br><br><br>  El equipo de <b>' + settings.SITIO + '</b> Gracias         </p>        </td>   </tr></table>'
            # EnviarEmailDef(titulo,msj,html,usuario.email)

            return HttpResponse('ok')
        return super(UsuarioCreateView, self).post(request,*args, **kwargs)



class UsuarioDeleteView(DeleteView):
    model = User
    success_url = "/usuario/"
    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(UsuarioDeleteView, self).dispatch(*args, **kwargs)
    def delete(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            user = User.objects.get(pk=request.POST['pk'])
            user.delete()
            return HttpResponse('ok')
        else:
            raise Http404




# def RegistroDef(request):
#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         Rname = request.POST.get('Rname')
#         Rusername = request.POST.get('Rusername')
#         Remail = request.POST.get('Remail')
#         Rpassword = request.POST.get('Rpassword')
#         try:
#             user = User.objects.get(username=Rusername)
#             msj='existeUser'
#             return HttpResponse(msj)            
#         except ObjectDoesNotExist:
#             try:
#                 user = User.objects.get(email=Remail)
#                 msj='existeEmail'
#                 return HttpResponse(msj)
#             except ObjectDoesNotExist:
#                 pass
#             # E instanciamos un objeto User, con el username y password
#             user_model = User.objects.create_user(username=Rusername, password=Rpassword)
#             # Añadimos el email
#             user_model.email = Remail
#             user_model.first_name= Rname
#             # Y guardamos el objeto, esto guardara los datos en la db.
#             user_model.save()
#             # Ahora, creamos un objeto UserProfile, aunque no haya incluido
#             # una imagen, ya quedara la referencia creada en la db.
#             user_profile = UserProfile()
#             # Al campo user le asignamos el objeto user_model
#             user_profile.user = user_model
#             # y le asignamos la photo (el campo, permite datos null)
#             #user_profile.photo = photo
#             # Por ultimo, guardamos tambien el objeto UserProfile
#             user_profile.save()
        
#             user = authenticate(username=Rusername, password=Rpassword)
#             AsignarDef(user.id)
#             titulo = 'Almorir.me verficacion de email'
#             msj = 'Saludos Gracias por utilizar los servicios de mensajeria post mortem de Almorir.me, en este momento su emnil no esta verificado de click en esiguente vinculo para verficar su email: Verificar email en Almorir.me  El equipo de radiowebdigital.com Gracias'
#             html = '<table style="width:600px;margin:auto"> <tr><td align="center" style="text-align:center;"><img src="http://almorir.me/static/img/logo250.png" alt="">      </td>   </tr>   <tr>        <td style="background:#ccc">            <p style="width:80%;margin:auto;padding:20px;font-size:1.5em;"> <b>Saludos</b><br> Gracias por utilizar los servicios de mensajería post mortem de <a href="http://almorir.me"> Almorir.me</a>, en este momento su <b>email no esta verificado</b> visite el siguiente enlace para verificar su email: <br> <br><a href="http://almorir.me/verificar-email/' + str(request.user.id) + '/">Verificar email en Almorir.me</a> <br><br>  El equipo de <b>Almorir.me</b> Gracias         </p>        </td>   </tr></table>'
#             EnviarEmailDef.apply_async((titulo,msj, html, Remail),countdown=10)
#             login(request, user)
#             return HttpResponse('ok')
#     else:
#         raise Http404

def CheckUserDef(request,username):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            user = User.objects.get(username=username)
            return HttpResponse('existeUser')
        except ObjectDoesNotExist:
            return HttpResponse('ok')
    raise Http404
   
def CheckEmailDef(request,email):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            user = User.objects.get(email=email)
            return HttpResponse('existeEmail')
        except ObjectDoesNotExist:
            return HttpResponse('ok')
    raise Http404
   




@login_required(login_url='/oops/')
def account(request):
    error = None
    name_message = password_message = email_message = ''
    change_name_form = ChangeNameForm(data=request.POST or None, instance=request.user)
    change_password_form = PasswordChangeForm(data=request.POST or None, user = request.user)
    change_email_form = ChangeEmailForm(data=request.POST or None, instance=request.user)
    if request.method == "POST":
    	if "change_name" in request.POST:
    		change_name_form = ChangeNameForm(data=request.POST, instance=request.user)
    		if change_name_form.is_valid():
    			change_name_form.save()
    			name_message = 'Se ha cambiado el nombre satisfactoriamente.'
    	else:
    		change_name_form = ChangeNameForm(instance=request.user)

    	if "change_password" in request.POST:
    		change_password_form = PasswordChangeForm(user=request.user)
    		if change_password_form.is_valid():
    			change_password_form.save()        
    			password_message = 'Your password has been changed.'
    	else:
    		change_password_form = PasswordChangeForm(user=request.user)

    	if "change_email" in request.POST:
            change_email_form = ChangeEmailForm(request.POST, instance=request.user)
            if change_email_form.is_valid():
                try:
                    user = User.objects.get(email=request.POST['email'])
                    if user:
                        email_message = 'El Email se encuentra registrado, no cambio'
                except ObjectDoesNotExist:
                    change_email_form.save()
                    email_message = 'El Email se ha cambiado satisfactoriamente.'
                    titulo = 'Cambio de Email'
                    msj = 'Saludos Gracias por utilizar los servicios de ' + settings.SITIO + ', Su Email principal cambio con exito:' 
                    html = '<table style="width:600px;margin:auto"><tr> <td style="background:#eeeeee"><p style="width:80%;margin:auto;padding:20px;font-size:1.5em;"> <b>Saludos</b><br> Gracias por utilizar los servicios de <a href="http://' + settings.SITIO + '">' + settings.SITIO + '</a>:<br><b>Su Email cambio con exito<br><br><br>  El equipo de <b>' + settings.SITIO + '</b> Gracias         </p>        </td>   </tr></table>'
                    EnviarEmailDef(titulo,msj,html,request.POST['email'])
                
    	else:
    		change_email_form = ChangeEmailForm(instance=request.user)
    return render(request,'account.html', 
                       {'change_name_form': change_name_form,
                        'change_email_form': change_email_form, 
                        'change_password_form': change_password_form,
                        'password_message': password_message,
                        'name_message': name_message,
                        'email_message': email_message,})

def Desbloqueo(request,nano):
    try:
        profile = UserProfile.objects.get(user_id=nano)
        if  profile.fallidos  == 3:
            profile.fallidos = 0
            profile.save()
        else:
            raise Http404
        return render(request,'desbloqueo.html')
    except ObjectDoesNotExist:
        raise Http404



def EnviarEmailDef(titulo,msj,html,email):
    subject, from_email, to = titulo, 'Bingos Marvel<jbroges@gmail.com>', email 
    msg = EmailMultiAlternatives(subject, msj, from_email, [to])
    msg.attach_alternative(html, "text/html")
    msg.send()

"""