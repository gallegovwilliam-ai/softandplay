from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import Messages, Messages_Ajax, sendMessage
urlpatterns = ([
    path('', Messages, name='messages'),    
    path('scroll/', Messages_Ajax, name='messages-scroll'),    
    path('send/', sendMessage, name='send-messages'),    
])