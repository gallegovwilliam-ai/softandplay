# -*- encoding: utf-8 -*-

from requests import request, HTTPError
from django.shortcuts import redirect
from django.urls import reverse
from django.core.files.base import ContentFile
from .models import UserProfile

def update_avatar(backend, user, response, details,is_new=False,*args,**kwargs):
	if is_new:
		profile = UserProfile.objects.create(user_id=user.id)
		profile.save()

 
		if backend.name == 'facebook':
			url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
			parametro={'type': 'large'}
		
		elif backend.name == 'twitter':
			url = response.get('profile_image_url').replace('_normal','')
			parametro = {}
		try:
			response = request('GET', url, params=parametro)
			response.raise_for_status()
		except HTTPError:
			pass
		else:
			profile = UserProfile.objects.get(user_id=user.id)
			profile.thumb.save('{0}_social.jpg'.format(user.username), ContentFile(response.content))
			profile.save()

