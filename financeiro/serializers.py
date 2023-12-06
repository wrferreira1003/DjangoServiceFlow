from rest_framework import serializers
from .models import Transacao, TransacaoAfiliadoAdministrador

class TransacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacao
        fields =  '__all__'

class ClienteSerializerAlteracao(serializers.ModelSerializer):    
    class Meta:
        model = Transacao
        fields = '__all__'

class TransacaoAfiliadoAdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransacaoAfiliadoAdministrador
        fields =  '__all__'