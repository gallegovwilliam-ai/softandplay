from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import PartidaList,PartidaCreate, Tablero, Tablero75, inicarPartida, inicarPartida75, JuegoEnLinea, Ultimas5, lobby75, \
PartidaUpdate, lobby, cardspartida, DeletePartida, DeletePartida75, PartidaList75, Partida75Create, Partida75Update, Ultimas575, JuegoEnLinea75, cardspartida75
urlpatterns = ([
    path('crear/', login_required(PartidaCreate), name='crear-partida'),    
    path('75/crear/', login_required(Partida75Create), name='crear-partida75'),    
    path('ultimas5/<int:pk>/', login_required(Ultimas5), name="ultimas5" ),
    path('75/ultimas5/<int:pk>/', login_required(Ultimas575), name="ultimas575" ),
    path('iniciar/<int:pk>', login_required(inicarPartida), name="inicarPartida" ),
    path('75/iniciar/<int:pk>', login_required(inicarPartida75), name="inicarPartida75" ),
    path('juego-en-linea/<int:pk>/', login_required(Tablero), name="tablero" ),
    path('75/juego-en-linea/<int:pk>/', login_required(Tablero75), name="tablero75" ),
    path('jugar/<int:pk>/', login_required(JuegoEnLinea), name="JuegoEnLinea" ),    
    path('75/jugar/<int:pk>/', login_required(JuegoEnLinea75), name="JuegoEnLinea75" ),    
    path('lobby/', login_required(lobby), name='lobby-partida'),    
    path('lobby75/', login_required(lobby75), name='lobby-partida75'),    
    path('delete/<int:pk>', login_required(DeletePartida), name='delete-partida'),    
    path('75/delete/<int:pk>', login_required(DeletePartida75), name='delete-partida75'),    
    path('update/<int:pk>/', login_required(PartidaUpdate), name='update-partida'),    
    path('75/update/<int:pk>/', login_required(Partida75Update), name='update-partida75'),    
    path('cards-panel/<int:pk>/<str:dni>/', login_required(cardspartida), name='cards-panel'),    
    path('75/cards-panel/<int:pk>/<str:dni>/', login_required(cardspartida75), name='cards-panel75'),    
    path('<slug:tag>/', login_required(PartidaList), name='partida-list'),    
    path('75/<slug:tag>/', login_required(PartidaList75), name='partida75-list'),    

    #path('delete/<int:pk>/', login_required(ClienteDelete), name='delete-cliente'),
    #path('update/<int:pk>/', login_required(ClienteUpdate), name='update-cliente'),    
    ])

