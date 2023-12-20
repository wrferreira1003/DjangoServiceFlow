# serializers.py dentro do seu app
from rest_framework import serializers
from .models import FinanciamentoImovel,Certidoes, Processos, Documento, ClientJob, FinanciamentoVeiculo, Cartorio, ClienteTerceiro, ClientEmpresarial, ConsultaServicosGeralCPF, ConsultaServicosGeralVeiculo
from Afiliados.models import AfiliadosModel
from Cliente.serializers import ClienteSerializer
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

#Serializer do modelo ClientJob
class ClientJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientJob
        fields = '__all__'

    #Retorno apenas dados que tem valores
    def to_representation(self, instance):
        result = super().to_representation(instance)

        if "data_admissao" in result:
            result["data_admissao"] = formatar_data(result['data_admissao'])

        return {key: value for key, value in result.items() if value is not None}

#Serializer do modelo FinanciamentoVeiculo
class FinanciamentoVeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanciamentoVeiculo
        fields = '__all__'
    
    #Retorno apenas dados que tem valores
    def to_representation(self, instance):
        result = super().to_representation(instance)
        return {key: value for key, value in result.items() if value is not None}

#Serializer do modelo FinanciamentoVeiculo
class FinanciamentoImovelSerializer(serializers.ModelSerializer):
    detalhes_produtos_ativos = serializers.JSONField(required=False)
    valores_aproximados_despesas = serializers.JSONField(required=False)
    
    class Meta:
        model = FinanciamentoImovel
        fields = '__all__'
    
    #Retorno apenas dados que tem valores
    def to_representation(self, instance):
        result = super().to_representation(instance)
        return {key: value for key, value in result.items() if value is not None}

#Serializer do modelo Cartorio
class CartorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartorio
        fields = '__all__'
    
    #Retorno apenas dados que tem valores
    def to_representation(self, instance):
        result = super().to_representation(instance)
        return {key: value for key, value in result.items() if value is not None}

#Serializer do modelo ClienteTerceiro
class ClienteTerceiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteTerceiro
        fields = '__all__'
    
    #Retorno apenas dados que tem valores
    def to_representation(self, instance):
        result = super().to_representation(instance)
        return {key: value for key, value in result.items() if value is not None}

#Serializer do modelo Certidoes
class ClienteCertidoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certidoes
        fields = '__all__'
    
    #Retorno apenas dados que tem valores
    def to_representation(self, instance):
        result = super().to_representation(instance)

        if "data_casamento" in result:
            result["data_casamento"] = formatar_data(result['data_casamento'])
        
        if "data_inicial" in result:
            result["data_inicial"] = formatar_data(result['data_inicial'])
        
        if "data_final" in result:
            result["data_final"] = formatar_data(result['data_final'])
        
        if "data_obito" in result:
            result["data_obito"] = formatar_data(result['data_obito'])

        return {key: value for key, value in result.items() if value is not None}

#Serializer do modelo ClientEmpresarial
class ClientEmpresarialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientEmpresarial
        fields = '__all__'
    
    #Retorno apenas dados que tem valores
    def to_representation(self, instance):
        result = super().to_representation(instance)

        if "data_abertura" in result:
            result["data_abertura"] = formatar_data(result['data_abertura'])
        
        return {key: value for key, value in result.items() if value is not None}

#Serializer do modelo Certidao
class CertidoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certidoes
        fields = '__all__'
    
    #Retorno apenas dados que tem valores
    def to_representation(self, instance):
        result = super().to_representation(instance)
        return {key: value for key, value in result.items() if value is not None}

#Serializer do modelo Documentos
class DocumentoSerializer(serializers.ModelSerializer):
    arquivo = serializers.FileField(validators=[validate_file_type, validate_file_size])
    class Meta:
        model = Documento
        fields = '__all__'

class NovoPedidoSerializer(serializers.ModelSerializer):
    documentos = DocumentoSerializer(many=True, required=False)
    cliente = serializers.PrimaryKeyRelatedField(queryset=AfiliadosModel.objects.filter(user_type='CLIENTE'), required=False)
    afiliado_relacionado = serializers.PrimaryKeyRelatedField(queryset=AfiliadosModel.objects.filter(user_type='AFILIADO'), required=False)

    
    class Meta:
        model = Processos
        fields = '__all__'
        
    def create(self, validated_data):
        with transaction.atomic():
            documentos_data = validated_data.pop('documentos', [])
            cliente = validated_data.pop('cliente', None)  # Adicione esta linha
            afiliado_relacionado = validated_data.pop('afiliado_relacionado', None)  # Adicione esta linha
                
            processo = Processos.objects.create(cliente=cliente, afiliado=afiliado_relacionado, **validated_data)

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
    clientes = ClienteSerializer(source='cliente',read_only=True)  # Alterado aqui
    afiliado = AfiliadoSerializerConsulta(read_only=True)
    funcionario = AfiliadoSerializerConsulta(read_only=True)
    servicos = ServicoSerializer(read_only=True)
    transacao = TransacaoSerializer(read_only=True)
    client_job = ClientJobSerializer(source='clientjob', read_only=True)  # Alterado aqui
    financiamento_veiculo = FinanciamentoVeiculoSerializer(source='financiamentoveiculo', read_only=True)  # Alterado aqui
    cartorio = CartorioSerializer(read_only=True)       # Alterado aqui
    cliente_terceiro = ClienteTerceiroSerializer(source='clienteterceiro', read_only=True)       # Alterado aqui
    client_empresarial = ClientEmpresarialSerializer(source='clientempresarial', read_only=True)       # Alterado aqui
    certidoes = CertidoesSerializer( read_only=True)
    financiamentoimovel = FinanciamentoImovelSerializer(read_only=True)
    
   
    class Meta:
        model = Processos
        fields = '__all__'


    #Retorno apenas dados que tem valores
    def to_representation(self, instance):
        result = super().to_representation(instance)

        #Chamando a funcao para ajustar o formato da Data
        if "data_pedido" in result:
            result["data_pedido"] = formatar_data(result['data_pedido'])
        
        if "data_nascimento" in result:
            result["data_nascimento"] = formatar_data(result['data_nascimento'])

        if "data_casamento" in result:
            result["data_casamento"] = formatar_data(result['data_casamento'])
        return {key: value for key, value in result.items() if value is not None}

class ClienteSerializerAlteracao(serializers.ModelSerializer):    
    class Meta:
        model = Processos
        fields = ['status']

class ClienteSerializerAlteracaoAdmAfiliado(serializers.ModelSerializer):    
    class Meta:
        model = Processos
        fields = ['status_adm_afiliado']

class AtualizaDocumentoSerializer(serializers.ModelSerializer):
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

class ConsultaServicosGeralCPFSerilizer(serializers.ModelSerializer):
    class Meta:
        model = ConsultaServicosGeralCPF
        fields = '__all__'

class ConsultaServicosGeralVeiculoSerilizer(serializers.ModelSerializer):
    class Meta:
        model = ConsultaServicosGeralVeiculo
        fields = '__all__'
