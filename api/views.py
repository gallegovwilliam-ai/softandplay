from rest_framework.response import Response
from .serializers import UserSerializer, PartidaSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from partidas.models import Partida
from cards.models import Impresion
import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.utils import timezone
class UserApi(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
class PartidaApi(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    now = timezone.localdate()
    queryset = Partida.objects.filter(fecha=now.strftime("%Y-%m-%d"),termino=False)
    serializer_class = PartidaSerializer

class CartomesApi(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    now = timezone.localdate()
    queryset = Partida.objects.filter(fecha=now.strftime("%Y-%m-%d"),termino=False)
    serializer_class = PartidaSerializer    
