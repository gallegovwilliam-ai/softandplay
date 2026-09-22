from django.urls import path
from .views import UserApi, PartidaApi
from rest_framework.authtoken import views

urlpatterns = ([
    path('crear-user/', UserApi.as_view(),  name='api-crear-user'),    
    path('partidas/', PartidaApi.as_view(),  name='api-partidas'),    
    path('generate-token/', views.obtain_auth_token),    
    ])

