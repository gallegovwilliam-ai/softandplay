from rest_framework import serializers
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from partidas.models import Partida


class UserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    def create(self, validate_data):
        instance = User()        
        instance.username = validate_data.get('username')
        instance.email = validate_data.get('email')
        instance.set_password(validate_data.get('password'))
        instance.save()            
        UserProfile.objects.create(user=instance,block='no',registered=True)
        return instance

    def validate_username(self,data):
        users = User.objects.filter(username=data)
        if users:
            raise serializers.ValidationError('Username existe')
        else:
            return data


class PartidaSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    fecha = serializers.CharField()
    descripcion = serializers.CharField()
    monto_carton = serializers.CharField()
    inicio = serializers.BooleanField()
 