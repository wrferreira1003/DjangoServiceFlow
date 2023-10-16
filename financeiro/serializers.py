from rest_framework import serializers
from .models import Transacao

class TransacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacao
        fields =  '__all__'

class ClienteSerializerAlteracao(serializers.ModelSerializer):    
    class Meta:
        model = Transacao
        fields = ['status']