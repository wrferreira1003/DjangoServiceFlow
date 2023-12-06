# serializers.py dentro do seu app
from rest_framework import serializers
from .models import Processos, Documento
from Afiliados.models import AfiliadosModel
from Cliente.models import Cliente
from financeiro.models import Transacao
from django.db import transaction
from validacoes import validate_file_type, validate_file_size
from datetime import datetime, date
from Servicos.models import Servico
from financeiro.models import Transacao
import os

#Funcao que formata a data para enviar ao front
def formatar_data(data_string, formato_entrada=None, formato_saida="%d/%m/%Y"):
    if data_string is None:
        return None
    
    formatos_possiveis = [
        "%Y-%m-%dT%H:%M:%S.%f%z",  # Formato ISO com fuso horário
        "%Y-%m-%d",                # Formato ano-mês-dia
    ]

    if formato_entrada:
        formatos_possiveis.insert(0, formato_entrada)

    for formato in formatos_possiveis:
        try:
            data_obj = datetime.strptime(data_string, formato)
            return data_obj.strftime(formato_saida)
        except ValueError:
            continue

    # Retorna a string original se nenhuma conversão funcionar
    return data_string

class DocumentoSerializer(serializers.ModelSerializer):
    arquivo = serializers.FileField(validators=[validate_file_type, validate_file_size])
    class Meta:
        model = Documento
        fields = '__all__'

class NovoPedidoSerializer(serializers.ModelSerializer):
    documentos = DocumentoSerializer(many=True, required=False)

    class Meta:
        model = Processos
        fields = '__all__'
        
    def create(self, validated_data):
        with transaction.atomic():
            documentos_data = validated_data.pop('documentos', [])

            processo = Processos.objects.create(**validated_data)

            for doc in documentos_data:
                Documento.objects.create(cliente=processo, **doc)

            return processo

class DocumentoSerializerConsulta(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'

class AfiliadoSerializerConsulta(serializers.ModelSerializer):
    class Meta:
        model = AfiliadosModel
        fields = [ 'id',
                   'nome', 
                   'telefone'
                ]
    
class NovoClienteSerializerConsulta(serializers.ModelSerializer):
    documentos = DocumentoSerializerConsulta(many=True, source='documento_set', read_only=True)
    afiliado = AfiliadoSerializerConsulta(read_only=True)
    
    class Meta:
        model = Processos
        fields = '__all__'
    
    #Retorno apenas dados que tem valores    
    def to_representation(self, instance):    
        representation = super().to_representation(instance)
        
        #Chamando a funcao para ajustar o formato da Data
        if "data_pedido" in representation:
            representation["data_pedido"] = formatar_data(representation['data_pedido'])
        #Chamando a funcao para ajustar o formato da Data
        if "data_nascimento" in representation:
            representation["data_nascimento"] = formatar_data(representation['data_nascimento'])
    
        if "data_casamento" in representation:
            representation["data_casamento"] = formatar_data(representation['data_casamento'])

        
        return {key: value for key, value in representation.items() if value not in [None, "", [], {}, "null"]}

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = '__all__' # Adicione outros campos se necessário

class TransacaoSerializer(serializers.ModelSerializer):
    servico = ServicoSerializer()
    class Meta:
        model = Transacao
        fields = '__all__'

class ClienteSerializerConsulta(serializers.ModelSerializer):
    documentos = DocumentoSerializerConsulta(many=True, source='documento_set', read_only=True)
    afiliado = AfiliadoSerializerConsulta(read_only=True)
    funcionario = AfiliadoSerializerConsulta(read_only=True)
    servicos = ServicoSerializer(read_only=True)
    transacao = TransacaoSerializer(read_only=True) 

    class Meta:
        model = Processos
        fields = '__all__'

class ClienteSerializerAlteracao(serializers.ModelSerializer):    
    class Meta:
        model = Processos
        fields = ['status']

class ClienteSerializerAlteracaoAdmAfiliado(serializers.ModelSerializer):    
    class Meta:
        model = Processos
        fields = ['status_adm_afiliado']

class AtualizaClienteSerializer(serializers.ModelSerializer):
    documentos = DocumentoSerializer(many=True, required=False)

    class Meta:
        model = Processos
        fields = '__all__'
        
    def update(self, instance, validated_data):
        with transaction.atomic():
            documentos_data = validated_data.pop('documentos', [])
            #print(validated_data.items())
            # Atualize os campos do cliente
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            # Adicione/Atualize os documentos associados
            for doc in documentos_data:
                # Supondo que você tenha um ID para cada documento
                # Se houver, atualize o documento existente; caso contrário, crie um novo
                doc_id = doc.pop('id', None)
                if doc_id:
                    Documento.objects.filter(id=doc_id).update(**doc)
                else:
                    Documento.objects.create(cliente=instance, **doc)

            return instance


