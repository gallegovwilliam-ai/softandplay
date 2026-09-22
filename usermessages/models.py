from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.humanize.templatetags.humanize import naturaltime

class Message(models.Model):
    user_emiter = models.ForeignKey(User, on_delete = models.CASCADE)
    message = models.TextField()
    readed = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False,default='2020-06-29')

    def save(self, *args, **kwargs):
        if not self.id:
        	fecha = timezone.now()
        	self.created_at = fecha
        return super(Message, self).save(*args, **kwargs)    

class userMessage(models.Model):
    message = models.ForeignKey(Message, on_delete = models.CASCADE)
    user_reciver = models.ForeignKey(User, on_delete = models.CASCADE)
    readed = models.BooleanField(default=False)
    url = models.CharField(max_length=255,default='x')


@receiver(post_save,sender=userMessage)
def messages_push(sender,instance,created,**kwargs):
	if created:
		channel_layer = get_channel_layer()
		day = naturaltime(instance.message.created_at)
		data = {
			'type': 'message',
			'timeago': str(day),
			'img': '/media/' + str(instance.message.user_emiter.userprofile.thumb),
			'user_emiter':instance.message.user_emiter.username,
			'username_emiter':instance.message.user_emiter.username,
	    	'message' : '<strong class="hidden-message">' + instance.message.user_emiter.username + ':</strong> ' + instance.message.message,  # Pass any data based on your requirement
	       	"url": instance.url, #str(reverse_lazy('cargar-video', kwargs={'pk':1}))
		}		# Trigger message sent to group
		async_to_sync(channel_layer.group_send)(
			str(instance.user_reciver.pk),  # Group Name, Should always be string
			{
				"type": "notify",   # Custom Function written in the consumers.py
				"text": data,
			},
		)  	
