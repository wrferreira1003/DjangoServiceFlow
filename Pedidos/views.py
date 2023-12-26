# Importando os pacotes necessarios
from rest_framework import status, generics
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ConsultaServicosGeralCPFSerilizer, ClienteCertidoesSerializer, ClienteTerceiroSerializer, CartorioSerializer, ClientJobSerializer, FinanciamentoVeiculoSerializer,ClienteSerializerAlteracaoAdmAfiliado, NovoPedidoSerializer,DocumentoSerializer, ClienteSerializerConsulta, ClienteSerializerAlteracao,AtualizaDocumentoSerializer,ClientEmpresarialSerializer, FinanciamentoImovelSerializer

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Certidoes, Processos, Documento, ClientJob, FinanciamentoVeiculo, ClientEmpresarial, ClienteTerceiro, Cartorio, FinanciamentoImovel, ConsultaServicosGeral
from Cliente.models import Cliente
from Cliente.serializers import ClienteSerializer, ClienteExistenteSerializer, UserSerializer
from Servicos.models import Servico
from financeiro.models import Transacao
from Afiliados.models import AfiliadosModel
from rest_framework.pagination import PageNumberPagination
import logging
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.core.exceptions import ValidationError
import json

logger = logging.getLogger('django')

#Criando uma classe de paginaçao que posso usar nas requisiçoes
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

#Funcao que cria ou atualiza um novo cliente na hora que uma nova solicitacao e feita.
def criar_ou_atualizar_cliente(data):
    # Verificar se o cliente existe
    cliente_existente = None
    if 'cpf' in data:
        cliente_existente = AfiliadosModel.objects.filter(cpf=data['cpf'], user_type='CLIENTE').first()
    print(cliente_existente)
    # Caso o cliente exista vamos atualizar os dados dele
    if cliente_existente:
        cliente_serializer = ClienteExistenteSerializer(instance=cliente_existente, data=data, partial=True)
     
    else:
        cliente_serializer = ClienteSerializer(data=data)
     
    if cliente_serializer.is_valid():
        try:
            cliente_obj = cliente_serializer.save()
            return cliente_obj.id, cliente_obj, cliente_existente is None
        except Exception as e:
            logger.error(f"Erro ao salvar o cliente: {e}")
            return None, False, False
    else:
        logger.error(f"Erro na validação dos dados do cliente: {cliente_serializer.errors}")
        return None, False, False

#Funcao que cria uma transacao no banco de dados
def criar_transacao(cliente_data,processo_obj, servico_id):
    logger.info("Iniciando a criação de uma transacao...")
    try:
        # ... seu código para criar ou atualizar cliente aqui ...
        cliente_instance = AfiliadosModel.objects.get(pk=cliente_data.id)
        
        afiliado = cliente_instance.afiliado_relacionado if cliente_instance.afiliado_relacionado else None
        afiliado_instance = AfiliadosModel.objects.get(pk=afiliado.id)
           
        pedido_instance = processo_obj
        
        servico_instance = Servico.objects.get(pk=servico_id)

        transacao_data = {
            "cliente": cliente_instance,
            "afiliado": afiliado_instance,
            "servico": servico_instance,
            "pedido": pedido_instance,
            "preco": servico_instance.preco,
            "FormaDePagamento": processo_obj.FormaDePagamento,
            "statusPagamento": 'Link de pagamento não disponivel'
        }
        logger.info(transacao_data)

        return Transacao.objects.create(**transacao_data)
    except Exception as e:
        logger.error(f"Erro ao criar transação: {e}")
        #print(e)
        return None

def criar_transacao_sem_cliente(cliente_data,processo_obj, servico_id):
    logger.info("Iniciando a criação de uma transacao...")
    
    try:
        cliente_id = cliente_data.get('id')
        cliente_instance = AfiliadosModel.objects.get(pk=cliente_id) if cliente_id else None
        
        if cliente_instance is None and cliente_data:
            afiliado = cliente_data.get('afiliado_relacionado', None)
            #print(afiliado)
        else:
            afiliado = cliente_instance.afiliado_relacionado if cliente_instance and cliente_instance.afiliado_relacionado else None
        
        afiliado_instance = AfiliadosModel.objects.get(pk=afiliado)
           
        pedido_instance = processo_obj
        
        servico_instance = Servico.objects.get(pk=servico_id)

        transacao_data = {
            "cliente": cliente_instance,
            "afiliado": afiliado_instance,
            "servico": servico_instance,
            "pedido": pedido_instance,
            "preco": servico_instance.preco,
            "FormaDePagamento": processo_obj.FormaDePagamento,
            "statusPagamento": 'Link de pagamento não disponivel'
        }
        logger.info(transacao_data)

        return Transacao.objects.create(**transacao_data)
    except Exception as e:
        logger.error(f"Erro ao criar transação: {e}")
        #print(e)
        return None
#Funcao que cria os Dados de trabalho do cliente
def criar_client_job(dados_client_job, processo_obj):
    
    client_job_serializer = ClientJobSerializer(data=dados_client_job)
    #print('dados client job',dados_client_job)

    if client_job_serializer.is_valid():
        #print('client job serializer',client_job_serializer)
        
        client_job_serializer.save(processo=processo_obj)
        return client_job_serializer
    else:
        # Pode levantar uma exceção ou tratar o erro conforme a necessidade
        logger.error(f"Erro na validação dos documentos: {client_job_serializer.errors}")
        raise ValidationError(f"Erro na validação do ClientJob: {client_job_serializer.errors}")

def criar_financiamento_imoveis(dados_client_job, processo_obj):
    
    client_job_serializer = FinanciamentoImovelSerializer(data=dados_client_job)
    #print('dados client job',dados_client_job)

    if client_job_serializer.is_valid():
        #print('client job serializer',client_job_serializer)
        
        client_job_serializer.save(processo=processo_obj)
        return client_job_serializer
    else:
        # Pode levantar uma exceção ou tratar o erro conforme a necessidade
        logger.error(f"Erro na validação dos documentos: {client_job_serializer.errors}")
        raise ValidationError(f"Erro na validação do Financiamento Imobiliario: {client_job_serializer.errors}")
#Funcao que cria os Dados de trabalho do cliente
def criar_client_Juridico(dados_client_juridico, processo_obj):
    
    client_juridico_serializer = ClientEmpresarialSerializer(data=dados_client_juridico)
    #print('dados client job',dados_client_job)

    if client_juridico_serializer.is_valid():
        #print('client job serializer',client_job_serializer)
        
        client_juridico_serializer.save(processo=processo_obj)
        return client_juridico_serializer
    else:
        # Pode levantar uma exceção ou tratar o erro conforme a necessidade
        logger.error(f"Erro na validação dos documentos: {client_juridico_serializer.errors}")
        raise ValidationError(f"Erro na validação do ClientJob: {client_juridico_serializer.errors}")

#Funcao que cria os Dados de financiamento do cliente
def criar_financiamento_veiculo(dados_financiamento, processo_obj):
    financiamento_serializer = FinanciamentoVeiculoSerializer(data=dados_financiamento)
    if financiamento_serializer.is_valid():
        financiamento_serializer.save(processo=processo_obj)
        return financiamento_serializer
    else:
        # Pode levantar uma exceção ou tratar o erro conforme a necessidade
        logger.error(f"Erro na validação do financiamentoVeiculo: {financiamento_serializer.errors}")
        raise ValidationError(f"Erro na validação do financiamentoVeiculo: {financiamento_serializer.errors}")

#Funcao que cria os Dados de Cartorio do cliente
def criar_cartorio(dados_cartorio, processo_obj):
    cartorio_serializer = CartorioSerializer(data=dados_cartorio)
    if cartorio_serializer.is_valid():
        cartorio_serializer.save(processo=processo_obj)
        return cartorio_serializer
    else:
        # Pode levantar uma exceção ou tratar o erro conforme a necessidade
        logger.error(f"Erro na validação do cartorio: {cartorio_serializer.errors}")
        raise ValidationError(f"Erro na validação do cartorio: {cartorio_serializer.errors}")

#Funcao que cria os Dados de terceiro dos clientes
def criar_cliente_terceiro(dados_cliente_terceiro, processo_obj):
    cliente_terceiro_serializer = ClienteTerceiroSerializer(data=dados_cliente_terceiro)
    if cliente_terceiro_serializer.is_valid():
        cliente_terceiro_serializer.save(processo=processo_obj)
        return cliente_terceiro_serializer
    else:
        # Pode levantar uma exceção ou tratar o erro conforme a necessidade
        logger.error(f"Erro na validação do clienteTerceiro: {cliente_terceiro_serializer.errors}")
        raise ValidationError(f"Erro na validação do clienteTerceiro: {cliente_terceiro_serializer.errors}")

#Funcao que cria os Dados de certidoes dos clientes
def criar_certidoes(dados_certidoes, processo_obj):
    certidoes_serializer = ClienteCertidoesSerializer(data=dados_certidoes)
    if certidoes_serializer.is_valid():
        certidoes_serializer.save(processo=processo_obj)
        return certidoes_serializer
    else:
        # Pode levantar uma exceção ou tratar o erro conforme a necessidade
        logger.error(f"Erro na validação do certidoes: {certidoes_serializer.errors}")
        raise ValidationError(f"Erro na validação do certidoes: {certidoes_serializer.errors}")

#funcao que ajusta subservicos
def extrair_subservico(subservico):
    # Já que subservico é uma string, não precisamos pegar o primeiro elemento de uma lista
    subservico_str = subservico.strip()

    # Dividimos a string pelo caractere '-' e removemos espaços em branco extras.
    partes = subservico_str.split('-')
    nome_subservico = partes[0].strip() if len(partes) > 0 else ''

    return nome_subservico

def Process_request_data(request):
    data = request.data.copy()  # Mudança aqui
    files = request.FILES
    documentos_data = []

    # Captura todos os documentos enviados
    for key, arquivo in files.items():
        if key.startswith('documentos'):
            index = key.split('[')[1].split(']')[0]  # pegar o índice dos documentos
            descricao = data.get(f'documentos[{index}].descricao')
            documentos_data.append({
                'descricao': descricao,
                'arquivo': arquivo
        })
    
    # Remover campos de documentos do data original para evitar problemas com o serializador
    for key in list(data.keys()):
        if key.startswith('documentos'):
            del data[key]

    # Incluindo os documentos processados na data
    data['documentos'] = documentos_data
    return data

def validate_documents(data):
    documentos_serializer = DocumentoSerializer(data=data.get('documentos', []), many=True)
    if documentos_serializer.is_valid():
        return True
    else:
        logger.error(f"Erro na validação dos documentos: {documentos_serializer.errors}")
        return False

def process_documents(files, data):
    documentos_data = []
    #print(files)
    # Captura todos os documentos enviados
    for key, arquivo in files.items():
        if key.startswith('documentos'):
            index = key.split('[')[1].split(']')[0]  # pegar o índice dos documentos
            descricao = arquivo.name
            documentos_data.append({
                'descricao': descricao,
                'arquivo': arquivo
        })
    #print(documentos_data)        
    # Remover campos de documentos do data original para evitar problemas com o serializador
    for key in list(data.keys()):
        if key.startswith('documentos'):
            del data[key]

    return documentos_data

def formatar_data_coluna(nome_coluna, data):
    valor_coluna = data.get(nome_coluna)
    if valor_coluna:
        data_formatada = formatar_data(valor_coluna[0] if isinstance(valor_coluna, list) else valor_coluna, '%d/%m/%Y')
        if data_formatada:
            data[nome_coluna] = data_formatada
        else:
            return Response({'error': f'Formato inválido para {nome_coluna}.'}, status=status.HTTP_400_BAD_REQUEST)
    return data

#Funcao que cria um novo pedido ou atualiza um pedido existente
def atualizar_ou_criar(serializer, instance, data):
    instance_fields = instance.get_field_names() if instance else []
    instance_data = {
        field: data.get(field) for field in instance_fields if field in data
    }
    if instance_data:
        instance_serializer = serializer(instance, data=instance_data, partial=True)
        if instance_serializer.is_valid():
            instance_serializer.save()
        else:
            print(instance_serializer.errors)
            return Response(instance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#----------------------------------------------------------------------------------------------#     
#Consultar os pedidos pelo id do cliente
class NovoClienteDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id, format=None):
        clientes = Processos.objects.filter(idCliente=id)
        if clientes.exists():
            serializer = ClienteSerializerConsulta(clientes, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

#Consultar todos os pedidos, pelo painel do administrado.        
class TodosClientesViewSemFiltro(ListCreateAPIView):
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    queryset = Processos.objects.all().order_by('-data_pedido')
    serializer_class = ClienteSerializerConsulta


class TodosClientesView(ListCreateAPIView):
    queryset = Processos.objects.all().order_by('-data_pedido')
    permission_classes = [IsAuthenticated]
    serializer_class = ClienteSerializerConsulta

#Excluir processos do banco de dados
class ClienteDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Processos.objects.all()
    serializer_class = ClienteSerializerConsulta
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

#Alteracao de status no banco de dados do campo AfiliadoCliente
class ClienteDetailViewAlteracao(UpdateAPIView):
    queryset = Processos.objects.all()
    serializer_class = ClienteSerializerAlteracao
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

#Alteracao de status no banco de dados do campo AdmAfiliado
class ClienteDetailViewAlteracaoStatusAdmAfiliado(UpdateAPIView):
    queryset = Processos.objects.all()
    serializer_class = ClienteSerializerAlteracaoAdmAfiliado
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

#Funcao para auxiliar na formatacao das datas antes de salvar
def formatar_data(data_string, formato_origem, formato_destino='%Y-%m-%d'):
    try:
        return datetime.strptime(data_string, formato_origem).strftime(formato_destino)
    except ValueError:
        return None

#Consultar os pedidos pelo id do afiliado
class PedidosPorAfiliadoListView(generics.ListAPIView):
    serializer_class = ClienteSerializerConsulta
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Este método irá retornar uma lista de pedidos para o afiliado especificado.
        O afiliado é determinado pelo `id` passado na URL.
        """
        afiliado_id = self.kwargs['afiliado_id']
        return Processos.objects.filter(afiliado__id=afiliado_id).order_by('-data_pedido')

class PedidosPorFuncionarioListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClienteSerializerConsulta  # ou o serializer apropriado
    
    
    def get_queryset(self):
        """
        Este método irá retornar uma lista de pedidos para o funcionário especificado.
        O funcionário é determinado pelo `id` passado na URL.
        """
        funcionario_id = self.kwargs['funcionario_id']
        return Processos.objects.filter(funcionario__id=funcionario_id).order_by('-data_pedido')  


class PedidosPorClienteListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClienteSerializerConsulta

    def get_queryset(self):
        """
        Este método irá retornar uma lista de pedidos para o afiliado especificado.
        O afiliado é determinado pelo `id` passado na URL.
        """
        cliente_id = self.kwargs['cliente_id']
        return Processos.objects.filter(cliente_id=cliente_id).order_by('-data_pedido')
    
@api_view(['DELETE'])
def delete_documento_api(request, documento_id):
    permission_classes = [IsAuthenticated]
    try:
        documento = Documento.objects.get(id=documento_id)
    except Documento.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "DELETE":
        documento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#------------------------Funcoes de criacao de processos---------------------------------------#    
#Criar um novo pedido com cliente e documentos dos processos cartorarios
@transaction.atomic # Isso garante que todas as operações de banco de dados sejam executadas ou nenhuma delas seja executada
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_cliente_com_relacionados(request):
    logger.info("Iniciando a criação do cliente e relacionados...")
    data = request.data.copy()  # Mudança aqui
    #print(data)
    # Chamada para a função que cria ou atualiza o cliente
    cliente_id, cliente_data, is_new = criar_ou_atualizar_cliente(data)
    
    try:
        # ... seu código para criar ou atualizar cliente aqui ...
        if cliente_id is None:
            logger.error("Erro ao criar ou atualizar cliente: cliente_id é None")
            return Response({"error": "Erro ao criar ou atualizar cliente."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Erro ao criar ou atualizar cliente: {str(e)}")
        return Response({"error": "Erro ao criar ou atualizar cliente."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Adicione o ID do cliente ao dicionário 'data'
    data['cliente'] = cliente_id 

    # Incluindo os documentos processados na data
    documentos_data = process_documents(request.FILES, data)
    data['documentos'] = documentos_data 

    # Vamos testar a validação dos documentos aqui
    doc_serializer = DocumentoSerializer(data=documentos_data, many=True)
    doc_serializer.is_valid(raise_exception=True)

    #Validacao e criacao do processo.
    #raise_exception=True: Isso faz com que o serializador levante uma exceção se a validação falhar
    processo_serializer = NovoPedidoSerializer(data=data) # Aqui você passa o data com os documentos
    processo_serializer.is_valid(raise_exception=True) # Aqui você testa a validação do processo e dos documentos
    
    
    processo_serializer.validated_data['documentos'] = documentos_data
    processo_obj = processo_serializer.save() # Aqui você obtém o objeto Processos criado


    # Chamada para a funcao para criar os dados do cartorio caso tenha essa informacao
    cartorio_data_fields = Cartorio.get_field_names()
    cartorio_data = {}
    for field in cartorio_data_fields:
        cartorio_data[field] = data.get(f'cartorio[{field}]', None)
    #print(cartorio_data)
    if cartorio_data and not all(value is None for value in cartorio_data.values()):
        try:
            criar_cartorio(cartorio_data, processo_obj)
        except ValueError as e:
            logger.error(f"Erro na criação do cartorio: {str(e)}")
            #(f"Erro na criação do cartorio: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
 
    # Chamada para a funcao para criar os dados do cliente terceiro caso tenha essa informacao
    cliente_terceiro_data_fields = ClienteTerceiro.get_field_names()
    cliente_terceiro_data = {}
    for field in cliente_terceiro_data_fields:
        cliente_terceiro_data[field] = data.get(f'cliente_terceiro[{field}]', None)
    #print(cliente_terceiro_data)
    if cliente_terceiro_data and not all(value is None for value in cliente_terceiro_data.values()):
        try:
            criar_cliente_terceiro(cliente_terceiro_data, processo_obj)
        except ValueError as e:
            logger.error(f"Erro na criação do cliente_terceiro: {str(e)}")
            #print(f"Erro na criação do cliente_terceiro: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
    # Chamada para a funcao para criar os dados das certidoes caso tenha essa informacao
    certidoes_data_fields = Certidoes.get_field_names()
    certidoes_data = {}
    for field in certidoes_data_fields:
        certidoes_data[field] = data.get(f'certidoes[{field}]', None)
    #print(certidoes_data)
    if certidoes_data and not all(value is None for value in certidoes_data.values()):
        try:
            criar_certidoes(certidoes_data, processo_obj)
        except ValueError as e:
            logger.error(f"Erro na criação do certidoes: {str(e)}")
            #print(f"Erro na criação do certidoes: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
   
    #Aqui criamos a instancia de transacao
    transacao_obj = criar_transacao(cliente_data, processo_obj, data.get('servico'))
    if not transacao_obj:
        logger.error("Erro ao criar transação. Serviço não encontrado.")
        return Response({"error": "Serviço não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

            
    return Response(processo_serializer.data, status=status.HTTP_201_CREATED)

#Criar um novo pedido com cliente e documentos dos processos cartorarios
@transaction.atomic # Isso garante que todas as operações de banco de dados sejam executadas ou nenhuma delas seja executada
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ClienteFinanciamentoVeiculo(request):
    logger.info("Iniciando a criação do cliente e relacionados...")
    data = request.data.copy()  # Mudança aqui

    # Chamada para a função que cria ou atualiza o cliente
    cliente_id, cliente_data, is_new = criar_ou_atualizar_cliente(data)
    if cliente_id is None:
        logger.error(f"Erro ao criar ou atualizar cliente")
        #print(e)
        return Response({"error": "Erro ao criar ou atualizar cliente."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Adicione o ID do cliente ao dicionário 'data'
    data['cliente'] = cliente_id 
    
    # Incluindo os documentos processados na data
    documentos_data = process_documents(request.FILES, data)
    data['documentos'] = documentos_data 

    # Vamos testar a validação dos documentos aqui
    doc_serializer = DocumentoSerializer(data=documentos_data, many=True)
    doc_serializer.is_valid(raise_exception=True)
 
        
    #Validacao e criacao do processo.
    #raise_exception=True: Isso faz com que o serializador levante uma exceção se a validação falhar
    processo_serializer = NovoPedidoSerializer(data=data) # Aqui você passa o data com os documentos
    processo_serializer.is_valid(raise_exception=True) # Aqui você testa a validação do processo e dos documentos
    
    processo_serializer.validated_data['documentos'] = documentos_data
    processo_obj = processo_serializer.save() # Aqui você obtém o objeto Processos criado

    #Aqui vamos verificar se é financiamento de veiculo e se for criamos a instancia de financiamento e job
    subservico = request.data.get('subservico', '')
    nome_subservico = extrair_subservico(subservico)
    # Funcao que cria as instancias de job e financiamento.
    if nome_subservico == "Financiamento Veicular":
        
        #Ajustando os dados que chegam do front end para o formato do banco de dados cliente_job
        client_job_fields = ClientJob.get_field_names() # Pegando os nomes dos campos do banco de dados
        client_job = {} # Criando um dicionario vazio
        for field in client_job_fields: #Percorrendo os campos do banco de dados
            client_job[field] = data.get(f'client_job[{field}]', None) #Adicionando os campos do banco de dados no dicionario vazio

        #Ajustando os dados que chegam do front end para o formato do banco de dados financiamento_veiculo
        financiamento_veiculo_fields = FinanciamentoVeiculo.get_field_names()
        financiamento_veiculo = {}
        for field in financiamento_veiculo_fields:
            financiamento_veiculo[field] = data.get(f'financiamento_veiculo[{field}]', None)

        cliente_juridico_fields = ClientEmpresarial.get_field_names() # Pegando os nomes dos campos do banco de dados
        #print(cliente_juridico_fields)
        cliente_juridico = {} # Criando um dicionario vazio
        for field in cliente_juridico_fields: #Percorrendo os campos do banco de dados
            cliente_juridico[field] = data.get(f'client_empresarial[{field}]', None) 
        #print(cliente_juridico)
                       
        try:
            #Verificando se algum dado do cliente juridico foi fornecido, os demais nao precisa pois sempre serao enviados, sao iguais para os dois caso
            if any(value is not None for value in cliente_juridico.values()): # Se sim, salve os dados do cliente empresarial
                criar_client_Juridico(cliente_juridico, processo_obj) # Chamando a funcao que cria o client_juridico
            
            criar_client_job(client_job, processo_obj) # Chamando a funcao que cria o client_job
            criar_financiamento_veiculo(financiamento_veiculo, processo_obj) # Chamando a funcao que cria o financiamento_veiculo
        except ValueError as e:
            logger.error(f"Erro na criação do client_job e financiamento_veiculo: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) 
            
    
    #Aqui criamos a instancia de transacao
    transacao_obj = criar_transacao(cliente_data, processo_obj, data.get('servico'))
    if not transacao_obj:
        logger.error("Erro ao criar transação. Serviço não encontrado.")
        return Response({"error": "Serviço não encontrado."}, status=status.HTTP_400_BAD_REQUEST)
            
    return Response(processo_serializer.data, status=status.HTTP_201_CREATED)

@transaction.atomic # Isso garante que todas as operações de banco de dados sejam executadas ou nenhuma delas seja executada
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ClienteFinanciamentoImoveis(request):
    logger.info("Iniciando a criação do cliente e relacionados...")
    data = request.data.copy()  # Mudança aqui

    # Chamada para a função que cria ou atualiza o cliente
    cliente_id, cliente_data, is_new = criar_ou_atualizar_cliente(data)
    if cliente_id is None:
        logger.error(f"Erro ao criar ou atualizar cliente")
        #print(e)
        return Response({"error": "Erro ao criar ou atualizar cliente."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Adicione o ID do cliente ao dicionário 'data'
    data['cliente'] = cliente_id 
    
    # Incluindo os documentos processados na data
    documentos_data = process_documents(request.FILES, data)
    data['documentos'] = documentos_data 

    # Vamos testar a validação dos documentos aqui
    doc_serializer = DocumentoSerializer(data=documentos_data, many=True)
    doc_serializer.is_valid(raise_exception=True)
 
        
    #Validacao e criacao do processo.
    #raise_exception=True: Isso faz com que o serializador levante uma exceção se a validação falhar
    processo_serializer = NovoPedidoSerializer(data=data) # Aqui você passa o data com os documentos
    processo_serializer.is_valid(raise_exception=True) # Aqui você testa a validação do processo e dos documentos
    
    processo_serializer.validated_data['documentos'] = documentos_data
    processo_obj = processo_serializer.save() # Aqui você obtém o objeto Processos criado

    json_str = data['financiamento_imoveis']
    #print(json_str)

    # Converter a string JSON em um dicionário
    financiamento_imoveis_data = json.loads(json_str)

    # Funcao que cria as instancias de job e financiamento imoveis.
    imoveis_fields = FinanciamentoImovel.get_field_names() # Pegando os nomes dos campos do banco de dados
    #print(cliente_juridico_fields)
    financiamento_imoveis = {} # Criando um dicionario vazio
    for field in imoveis_fields: #Percorrendo os campos do banco de dados
        financiamento_imoveis[field] = financiamento_imoveis_data.get(field, None) 
    #print(financiamento_imoveis)               
    try:        
        criar_financiamento_imoveis(financiamento_imoveis, processo_obj) # Chamando a funcao que cria o client_job
    except ValueError as e:
        logger.error(f"Erro na criação do Financiamento de Imoveis: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) 
            
    
    #Aqui criamos a instancia de transacao
    transacao_obj = criar_transacao(cliente_data, processo_obj, data.get('servico'))
    if not transacao_obj:
        logger.error("Erro ao criar transação. Serviço não encontrado.")
        return Response({"error": "Serviço não encontrado."}, status=status.HTTP_400_BAD_REQUEST)
            
    return Response(processo_serializer.data, status=status.HTTP_201_CREATED)

#Atualizar os dados do cliente 
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def AtualizaClienteView(request, id):  # Adicionando cliente_id para identificar o registro 
    try:
        processo = Processos.objects.get(pk=id)  # Obtenha o cliente pelo ID
        cliente = AfiliadosModel.objects.get(pk=processo.cliente.id, user_type='CLIENTE')  # Obtenha o cliente pelo ID
    except Processos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    #obter o ClientJob e o FinanciamentoVeiculo associados, ou defina-os como None se eles não existirem
    client_job = ClientJob.objects.filter(processo=processo).first()
    financiamento_veiculo = FinanciamentoVeiculo.objects.filter(processo=processo).first()
    client_empresarial = ClientEmpresarial.objects.filter(processo=processo).first()
    cliente_terceiro = ClienteTerceiro.objects.filter(processo=processo).first()
    cartorio = Cartorio.objects.filter(processo=processo).first()
    certidoes = Certidoes.objects.filter(processo=processo).first()
    imoveis = FinanciamentoImovel.objects.filter(processo=processo).first()

   
    
    data = request.data.copy()

   
    #Ajustes das datas antes de salvar no banco de dados
    #data_nascimento = formatar_data_coluna('data_nascimento', data)
    #if isinstance(data_nascimento, Response):
    #    return data_nascimento
    
    data_casamento = formatar_data_coluna('data_casamento', data)
    if isinstance(data_casamento, Response):
        return data_casamento
    
    data_inicial = formatar_data_coluna('data_inicial', data)
    if isinstance(data_inicial, Response):
        return data_inicial
    
    data_final = formatar_data_coluna('data_final', data)
    if isinstance(data_final, Response):
        return data_final

    data_obito = formatar_data_coluna('data_obito', data)
    if isinstance(data_obito, Response):
        return data_obito

    #data_admissao = formatar_data_coluna('data_admissao', data)
    #if isinstance(data_admissao, Response):
    #    return data_admissao 

    data_abertura = formatar_data_coluna('data_abertura', data)
    if isinstance(data_abertura, Response):
        return data_abertura          
    
    files = request.FILES

    documentos_data = []

    # Captura todos os documentos enviados
    for key, arquivo in files.items():
        if key.startswith('documentos'):
            index = key.split('[')[1].split(']')[0]
            descricao = data.get(f'documentos[{index}].descricao')
            documentos_data.append({
                'descricao': descricao,
                'arquivo': arquivo
            })

    # Atualizando os dados dos Clientes
    cliente_serializer = ClienteSerializer(cliente, data=data, partial=True)  # Crie um novo serializer para o cliente
    if cliente_serializer.is_valid():
        cliente_serializer.save()  # Salve os dados atualizados
    else:
        return Response(cliente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Remover campos de documentos do data original para evitar problemas com o serializador
    for key in list(data.keys()):
        if key.startswith('documentos'):
            del data[key]

    data['documentos'] = documentos_data

    
    documents_serializer = AtualizaDocumentoSerializer(processo, data=data, partial=True)  
    if documents_serializer.is_valid():
        documents_serializer.validated_data['documentos'] = documentos_data
        documents_serializer.save()
    else:
        return Response(documents_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # Atualize ou crie o ClientJob
    resposta = atualizar_ou_criar(ClientJobSerializer, client_job, data)
    if isinstance(resposta, Response):
        return resposta
    # Atualize ou crie o FinanciamentoVeiculo
    resposta = atualizar_ou_criar(FinanciamentoVeiculoSerializer, financiamento_veiculo, data)
    if isinstance(resposta, Response):
        return resposta
    # Atualize ou crie o ClientEmpresarial
    resposta = atualizar_ou_criar(ClienteCertidoesSerializer,   certidoes , data)
    if isinstance(resposta, Response):
        return resposta
    # Atualize ou crie o ClientEmpresarial
    resposta = atualizar_ou_criar(ClienteTerceiroSerializer,   cliente_terceiro , data)
    if isinstance(resposta, Response):
        return resposta
    # Atualize ou crie o ClientEmpresarial
    resposta = atualizar_ou_criar(CartorioSerializer,   cartorio , data)
    if isinstance(resposta, Response):
        return resposta
    # Atualize ou crie o ClientEmpresarial
    resposta = atualizar_ou_criar(ClientEmpresarialSerializer,   client_empresarial , data)
    if isinstance(resposta, Response):
        return resposta
    # Atualize ou crie o FinanciamentoImovel
    #print(data)
    resposta = atualizar_ou_criar(FinanciamentoImovelSerializer, imoveis, data)
    if isinstance(resposta, Response):
        #print(resposta)
        return resposta
    
    
    return Response(cliente_serializer.data, status=status.HTTP_200_OK)

#Recebe os processos onde o cliente nao e cadastrado como usuario no sistema de clientes
@transaction.atomic
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ClienteSemCadastroView(request):
    try:
        logger.info("Iniciando a criação do cliente")
        data = request.data.copy()  # Mudança aqui

        # Chamada para a função que cria ou atualiza o cliente
        cliente_id, cliente_data, is_new = criar_ou_atualizar_cliente(data)
        if cliente_id is None:
            logger.error(f"Erro ao criar ou atualizar cliente")
            #print(e)
            return Response({"error": "Erro ao criar ou atualizar cliente."}, status=status.HTTP_400_BAD_REQUEST)
    
        # Adicione o ID do cliente ao dicionário 'data'
        data['cliente'] = cliente_id 
    
        # Incluindo os documentos processados na data
        documentos_data = process_documents(request.FILES, data)
        data['documentos'] = documentos_data 

        # Vamos testar a validação dos documentos aqui
        doc_serializer = DocumentoSerializer(data=documentos_data, many=True)
        doc_serializer.is_valid(raise_exception=True)
 
        
        #Validacao e criacao do processo.
        #raise_exception=True: Isso faz com que o serializador levante uma exceção se a validação falhar
        processo_serializer = NovoPedidoSerializer(data=data) # Aqui você passa o data com os documentos
        processo_serializer.is_valid(raise_exception=True) # Aqui você testa a validação do processo e dos documentos
    
        processo_serializer.validated_data['documentos'] = documentos_data
        processo_obj = processo_serializer.save() # Aqui você obtém o objeto Processos criado

        #Aqui criamos a instancia de transacao
        transacao_obj = criar_transacao(cliente_data, processo_obj, data.get('servico'))
        if not transacao_obj:
            logger.error("Erro ao criar transação. Serviço não encontrado.")
            return Response({"error": "Serviço não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(processo_serializer.data, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        logger.error("Erro de validação: %s", e.detail)
        return Response({"error": str(e.detail)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error("Erro desconhecido: %s", str(e))
        return Response({"error": "Ocorreu um erro desconhecido."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#criar uma nova consulta simples sem armazenar o cliente no banco de dados, apenas a criacao da consulta juntamente com a transacao financeira
class ConsultaSimplesServicosView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data)
        

        #Validacao e criacao do processo.
        #raise_exception=True: Isso faz com que o serializador levante uma exceção se a validação falhar
        processo_serializer = NovoPedidoSerializer(data=data) # Aqui você passa o data com os documentos
        processo_serializer.is_valid(raise_exception=True) # Aqui você testa a validação do processo e dos documentos
        processo_obj = processo_serializer.save() # Aqui você obtém o objeto Processos criado

        #Aqui criamos a instancia de transacao
        transacao_obj = criar_transacao_sem_cliente(data, processo_obj, data.get('servico'))
        print(processo_obj)
        if not transacao_obj:
            logger.error("Erro ao criar transação. Serviço não encontrado.")
            return Response({"error": "Serviço não encontrado."}, status=status.HTTP_400_BAD_REQUEST)
        
        #Criacao da consulta simples
        data['servico'] = transacao_obj.servico.id
        data['processo'] = processo_obj.id
        serializer = ConsultaServicosGeralCPFSerilizer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data.copy()
        
        #Recebendo o id do processo no corpo da requisição
        consulta_id = data.get('id')
        if not consulta_id:
            return Response({"error": "ID da consulta não informado."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            consulta = ConsultaServicosGeral.objects.get(id=consulta_id)
        except:
            return Response({"error": "Consulta não encontrada."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ConsultaServicosGeralCPFSerilizer(consulta, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmprestimoEmGeralViewSet(APIView):
    permission_classes = [IsAuthenticated]
    pass
    
        