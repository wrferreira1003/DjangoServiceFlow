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
        FIELD_NAME_MAPPING = {
            'data_pedido': 'Data do Pedido',
            "idCliente": "Registro Cliente",
            "nome": "Nome",
            "email": "Email",
            "telefone": "Telefone",
            "RegistroGeral": "RG",
            "cpf": "CPF",
            "estado": "Estado",
            "endereco": "Endereço",
            "cidade": "Cidade",
            "bairro": "Bairrro",
            "cep": "CEP",
            "status": "Status do Processo",
            "servico": "Serviço Solicitado",
            "subservico": "SubServiço Solicitado",
            "nomeEnvolvido": "Nome do Envolvido",
            "sobrenomeEnvolvido": "Sobrenome do Envolvido",
            "RegistroGeralEnvolvido": "RG do Envolvido",
            "cpfEnvolvido": "CPF do Envolvido",
            "estado_civil": "Estado Civil",
            "profissao": "Profissao",
            "data_nascimento": "Data Nascimento",
            "nomeCartorioFirmaReconhecida": "NomeCartorioFirmaReconhecida",
            "estadoCartorioFirmaReconhecida": "EstadoCartorioFirmaReconhecida",
            "livroCartorioFirmaReconhecida": "LivroCartorioFirmaReconhecida",
            "nomeCartorio": "NomeCartorio",
            "estadoCartorio": "EstadoCartorio",
            "cidadeCartorio": "CidadeCartorio",
            "livroCartorio":"LivroCartório",
            "folhaCartorio": "FolhaCartório",
            "termo": "Termo",
            "tipoDeEntrega": "TipoDeEntrega",
            "FormaDePagamento": "Forma de Pagamento do Serviço",
            "conjugue1":"Conjugue1",
            "conjugue2":"Conjugue2",
            "data_casamento": "Data casamento",
            "data_obito": "Data óbito",
            "nome_falecido": "Nome do falecido",
            "data_inicial": "Data inicial",
            "data_final": "Data final",
            "filiacao1": "Filiação1",
            "filiacao2": "Filiação2",
            "Observacoes": "Observação",
            "temFilhosMenores":"TemFilhosMenores",
            "temBens":"TemBens",
            "filhoIncapaz":"FilhoIncapaz",
            # adicione outros campos aqui conforme necessário
        }
        
        representation = super().to_representation(instance)

         # Renomear campos conforme o mapeamento
        for field, new_name in FIELD_NAME_MAPPING.items():
            if field in representation:
                representation[new_name] = representation.pop(field)
        
        if "Data do Pedido" in representation:
            # Se já for um objeto de data, formate diretamente
            if isinstance(representation["Data do Pedido"], (datetime, date)):
                formatted_date = representation["Data do Pedido"].strftime("%d/%m/%Y")
            # Se for uma string, converta para data primeiro e depois formate
            else:
                date_obj = datetime.strptime(representation["Data do Pedido"], "%Y-%m-%dT%H:%M:%S.%f%z")
                formatted_date = date_obj.strftime("%d/%m/%Y")

            representation["Data do Pedido"] = formatted_date

        if "Data de Nascimento" in representation and representation["Data de Nascimento"]:
            # Se já for um objeto de data, formate diretamente
            if isinstance(representation["Data de Nascimento"], (datetime, date)):
                formatted_date = representation["Data de Nascimento"].strftime("%d/%m/%Y")
            # Se for uma string, converta para data primeiro e depois formate
            else:
                date_obj = datetime.strptime(representation["Data de Nascimento"], "%Y-%m-%d")  # Usando o formato YYYY-MM-DD
                formatted_date = date_obj.strftime("%d/%m/%Y")

            representation["Data de Nascimento"] = formatted_date

        if "Data casamento" in representation and representation["Data casamento"]:
            # Se já for um objeto de data, formate diretamente
            if isinstance(representation["Data casamento"], (datetime, date)):
                formatted_date = representation["Data casamento"].strftime("%d/%m/%Y")
            # Se for uma string, converta para data primeiro e depois formate
            else:
                date_obj = datetime.strptime(representation["Data casamento"], "%Y-%m-%d")  # Usando o formato YYYY-MM-DD
                formatted_date = date_obj.strftime("%d/%m/%Y")

            representation["Data casamento"] = formatted_date

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


