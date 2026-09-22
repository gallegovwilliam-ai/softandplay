from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import RegisterForm, CompleteRegistre, login, UsersList, UserUpdate,UserDelete, PendientesList, Solicitud, Aprobar, validar_email, solicitar_validacion
urlpatterns = ([
    #path('/', login_required(StatisticsEvaluationsPlayer), name='statistics-players'),
    path('password-reset/',auth_views.PasswordResetView.as_view(
    	template_name='password_reset.html',
    	html_email_template_name="email_reset_password.html"),name='password-reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ),
         name='password_reset_complete'),

    path('register-form', RegisterForm, name='register-form'),    
    path('register', CompleteRegistre, name='register'),    
    path('loguin-form', login, name='login-form'),    
    path('', login_required(UsersList), name='users-list'),    
    path('pendientes/', login_required(PendientesList), name='pendiente-list'),    
    path('update/<int:pk>/', login_required(UserUpdate), name='user-update'),    
    path('aprobar/<int:pk>/', login_required(Aprobar), name='aprobar'),    
    path('solicitud/<int:pk>/', login_required(Solicitud), name='solicitud'),    
    path('delete/<int:pk>/', login_required(UserDelete), name='user-delete'),    
    path('solicitar-validacion/', login_required(solicitar_validacion), name='solicitar_validacion'),
    path('validar-email/<uidb64>/<token>/', validar_email, name='validar_email'),    
])