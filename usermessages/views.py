from django.shortcuts import render,Http404, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import userMessage, Message
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.contrib.humanize.templatetags.humanize import naturaltime
import json
# Create your views here.

class  Messages(ListView):
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			raise Http404
		return super().dispatch(request, *args, **kwargs)
	model = userMessage
	template_name = 'messages.html'
	def get_queryset(self, *args, **kwargs):
		if self.request.user.is_superuser:
			mjs = userMessage.objects.filter(user_reciver=self.request.user).values('message__user_emiter__username').distinct()
		else:
			mjs = User.objects.filter(is_superuser=True).values('username')
		return mjs

#userMessage.objects.filter(Q(user_reciver=self.request.user) | Q(message__user_emiter=self.request.user)).order_by('-id')
		
Messages = Messages.as_view()


class  Messages_Ajax(ListView):
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			raise Http404
		return super().dispatch(request, *args, **kwargs)
	model = userMessage
	template_name = 'messages_scroll.html'
	paginate_by = 10
	def get_queryset(self, *args, **kwargs):
		return userMessage.objects.filter(Q(message__user_emiter__username=self.request.user.username,user_reciver__username=self.request.GET.get('username')) | Q(message__user_emiter__username=self.request.GET.get('username'),user_reciver__username=self.request.user.username) ).order_by('-id')
#userMessage.objects.filter(Q(user_reciver=self.request.user) | Q(message__user_emiter=self.request.user)).order_by('-id')
Messages_Ajax = Messages_Ajax.as_view()


@login_required
def sendMessage(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
		user_emiter = request.user
		user_reciver = User.objects.get(username=request.POST['user_reciver'])
		if user_reciver.pk == request.user.pk:
			raise Http404
		m = Message.objects.create(message=request.POST['message'],user_emiter=user_emiter)
		userMessage.objects.create(message=m, user_reciver=user_reciver)
		data = {
			'user_emiter': request.user.username,
			'img': '/media/' + str(request.user.userprofile.thumb),
			'message': request.POST['message'],
			'timeago':  naturaltime(m.created_at)
		}
		return JsonResponse(data)
	else:
		raise Http404