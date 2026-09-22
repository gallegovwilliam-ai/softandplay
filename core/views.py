from django.shortcuts import render, redirect, HttpResponse
from django.urls import  reverse_lazy
from django.contrib.auth.decorators import login_required
from notifications.models import Notification
from usermessages.models import Message, userMessage
from django.contrib.auth.models import User
import  datetime
from cards.models import Impresion, Impresion75
from partidas.models import Partida, Partida75
from configuracion.models import Config
from django.utils import timezone
# Create your views here.

@login_required
def home(request):
	obj, created = Config.objects.get_or_create(pk=1)
	resellers = None
	resellers75 = None
	#django_rq.enqueue(SendMail,user=request.user)
	if not request.user.userprofile.registered:
		return redirect(reverse_lazy('register'))
	if request.user.userprofile.block == 'si':
		return redirect('/logout/')
	solicitudes = User.objects.filter(is_active=True,userprofile__block='si').count()
	partida = Partida.objects.filter(fecha=timezone.localdate(),termino=False).order_by('partida')
	if partida:
		if request.user.is_superuser:
			vendidos = Impresion.objects.filter(propietario__partida = partida[0]).count()
			resellers = User.objects.filter(is_active=True,userprofile__user_type="Revendedor")
		elif request.user.is_staff:
			vendidos = Impresion.objects.filter(propietario__partida = partida[0],propietario__user=request.user).count()
			resellers = []
		if request.user.userprofile.user_type == 'Usuario':
			vendidos = Impresion.objects.filter(propietario__partida = partida[0]).count()
		acumulado = vendidos * partida[0].monto_carton
		revendedores = []
		partida_id = partida[0].id
		if resellers:
			for r in resellers:
				revendedores.append({'user':r,'vendidos': Impresion.objects.filter(propietario__partida = partida[0],propietario__user=r).count()})
	else:
		vendidos = 0
		acumulado = 0
		revendedores = []
		partida_id = 0

	partida75 = Partida75.objects.filter(fecha=timezone.localdate(),termino=False).order_by('partida')
	if partida75:
		if request.user.is_superuser:
			vendidos75 = Impresion75.objects.filter(propietario__partida = partida75[0]).count()
			resellers75 = User.objects.filter(is_active=True,userprofile__user_type="Revendedor")
		elif request.user.is_staff:
			vendidos75 = Impresion75.objects.filter(propietario__partida = partida75[0],propietario__user=request.user).count()
			resellers75 = []
		if request.user.userprofile.user_type == 'Usuario':
			vendidos75 = Impresion75.objects.filter(propietario__partida = partida75[0]).count()

		acumulado75 = vendidos75 * partida75[0].monto_carton
		revendedores75 = []
		partida75_id = partida75[0].id
		if resellers75:
			for r in resellers75:
				revendedores75.append({'user':r,'vendidos': Impresion75.objects.filter(propietario__partida = partida75[0],propietario__user=r).count()})
	else:
		vendidos75 = 0
		acumulado75 = 0
		revendedores75 = []
		partida75_id = 0

	return render(request, 'dashboard.html',{
												'solicitudes':solicitudes,
												'vendidos':vendidos,
												'partida':partida_id,
												'acumulado':acumulado,
												'revendedores':revendedores,
												'vendidos75':vendidos75,
												'partida75':partida75_id,
												'acumulado75':acumulado75,
												'revendedores75':revendedores75
											})

def Notify_test(request):
	if request.method != 'POST' or not request.user.is_superuser:
		return HttpResponse(status=404)
	mjs = Message.objects.create(user_emiter=request.user,message="haora")
	userMessage.objects.create(message=mjs, user_reciver=request.user)
	return HttpResponse('ok')

