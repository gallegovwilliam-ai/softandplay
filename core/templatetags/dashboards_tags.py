from django import template
import re
from notifications.models import Notification
from usermessages.models import Message, userMessage
from partidas.models import Partida, Partida75
import datetime
from django.utils import timezone
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.inclusion_tag('tags/partidas_tag.html')
def partidasDia(user):
    p = Partida.objects.filter(fecha=timezone.localdate(),termino=False)
    return {"partidasDia":p,'user':user}

@register.inclusion_tag('tags/partidas75_tag.html')
def partidasDia75(user):
    p = Partida75.objects.filter(fecha=timezone.localdate(),termino=False)
    return {"partidasDia":p,'user':user}

@register.inclusion_tag('tags/menu_tag.html')
def menu(user):
    return {"user":user}

@register.inclusion_tag('tags/nav_settings.html')
def nav_settings(user):
    return {"user":user}

@register.inclusion_tag('tags/nav_inbox.html')
def nav_inbox(user):
    return {
    	"messages":userMessage.objects.filter(user_reciver=user,readed=False).order_by('-pk')[:5],
    	"count_message":userMessage.objects.filter(user_reciver=user,readed=False).count()
    	}

@register.inclusion_tag('tags/nav_notifications.html')
def nav_notifications(user):
    return {
    	"notifications":Notification.objects.filter(user=user,readed=False).order_by('-pk')[:5],
    	"count_notify":Notification.objects.filter(user=user,readed=False).count()
    	}



"""
@register.inclusion_tag('tags/register.html')
def registerUser(Uform, Pform):
    return {"Uform":Uform, "Pform":Pform}

@register.inclusion_tag('tags/message.html')
def message(message):
    return {'message':message}

"""
