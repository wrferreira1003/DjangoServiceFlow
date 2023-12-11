# Importando os pacotes necessarios
from rest_framework import status, generics
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ClienteCertidoesSerializer, ClienteTerceiroSerializer, CartorioSerializer, ClientJobSerializer, FinanciamentoVeiculoSerializer,ClienteSerializerAlteracaoAdmAfiliado, NovoPedidoSerializer,DocumentoSerializer, ClienteSerializerConsulta,NovoClienteSerializerConsulta, ClienteSerializerAlteracao,AtualizaClienteSerializer,ClientEmpresarialSerializer

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Certidoes, Processos, Documento, ClientJob, FinanciamentoVeiculo, ClientEmpresarial, ClienteTerceiro, Cartorio
from Cliente.models import Cliente
from Cliente.serializers import ClienteSerializer, ClienteExistenteSerializer
from Servicos.models import Servico
from financeiro.models import Transacao
from Afiliados.models import AfiliadosModel
from rest_framework.pagination import PageNumberPagination
import logging
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.core.exceptions import ValidationError

logger = logging.getLogger('django')

#Criando uma classe de paginaçao que posso usar nas requisiçoes
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

#Funcao que cria ou atualiza um novo cliente na hora que uma nova solicitacao e feita.
def criar_ou_atualizar_cliente(data):
    #Verificar se o cliente existe
    cliente_existente = None
    if 'cpf' in data:
        cliente_existente = Cliente.objects.filter(cpf=data['cpf']).first()

    #Caso o cliente existe vamos atualizar os dados dele
    if cliente_existente:
        cliente_serializer = ClienteExistenteSerializer(instance=cliente_existente, data=data, partial=True)
    else:
        cliente_serializer = ClienteSerializer(data=data)
    
    if cliente_serializer.is_valid(raise_exception=True):
        cliente_serializer.save()
        return cliente_serializer.data, cliente_existente is None

    return None, False

#Funcao que cria uma transacao no banco de dados
def criar_transacao(cliente_data,processo_obj, servico_id):
    logger.info("Iniciando a criação de uma transacao...")
    try:
        cliente_instance = Cliente.objects.get(id=cliente_data.get('id'))

        #afiliado_instance = AfiliadosModel.objects.get(id=cliente_data.get('afiliado'))
        afiliado_id = cliente_data.get('afiliado')
        if afiliado_id:
            afiliado_instance = AfiliadosModel.objects.get(id=afiliado_id)
        else:
            afiliado_instance = None
        
        pedido_instance = Processos.objects.get(id=processo_obj.id)
        servico_instance = Servico.objects.get(pk=servico_id)

        servico_obj = Servico.objects.get(pk=servico_id)
        preco = servico_obj.preco

        transacao_data = {
            "cliente": cliente_instance,
            "afiliado": afiliado_instance,  # Assumindo que o cliente tem um campo afiliado
            "servico": servico_instance,
            "pedido": pedido_instance,  # Assumindo que a relação OneToOne entre Processos e Transacao é essa
            "preco": preco,  # Supondo que o modelo Servico tenha um campo chamado "valor"
            "FormaDePagamento": processo_obj.FormaDePagamento,  # você pode definir isso conforme necessário
            "statusPagamento": 'Link de pagamento não disponivel'
        }
        logger.info(transacao_data)

        return Transacao.objects.create(**transacao_data)
    except Exception as e:
        logger.error(f"Erro ao criar transação: {e}")
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

def create_process(data, cliente_data):
    processo_data = data.get('processo', {})
    processo_data['cliente'] = cliente_data['id']
    processo_serializer = ProcessoSerializer(data=processo_data)
    if processo_serializer.is_valid():
        processo_obj = processo_serializer.save()
        return processo_obj
    else:
        logger.error(f"Erro na validação do processo: {processo_serializer.errors}")
        return None

def process_documents(files, data):
    documentos_data = []
    print(files)
    # Captura todos os documentos enviados
    for key, arquivo in files.items():
        if key.startswith('documentos'):
            index = key.split('[')[1].split(']')[0]  # pegar o índice dos documentos
            descricao = arquivo.name
            documentos_data.append({
                'descricao': descricao,
                'arquivo': arquivo
        })
    print(documentos_data)        
    # Remover campos de documentos do data original para evitar problemas com o serializador
    for key in list(data.keys()):
        if key.startswith('documentos'):
            del data[key]

    return documentos_data

def build_process_data(data, model):
    data_fields = model.get_field_names()
    data_obj = {}
    for field in data_fields:
        data_obj[field] = data.get(field, None)
    return data_obj

#----------------------------------------------------------------------------------------------#     
#Consultar os pedidos pelo id do cliente
class NovoClienteDetailView(APIView):

    def get(self, request, id, format=None):
        clientes = Processos.objects.filter(idCliente=id)
        if clientes.exists():
            serializer = NovoClienteSerializerConsulta(clientes, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

#Consultar todos os pedidos, pelo painel do administrado.        
class TodosClientesViewSemFiltro(ListCreateAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = Processos.objects.all()
    serializer_class = ClienteSerializerConsulta

class TodosClientesView(ListCreateAPIView):
    queryset = Processos.objects.all()
    serializer_class = NovoClienteSerializerConsulta

#Excluir processos do banco de dados
class ClienteDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Processos.objects.all()
    serializer_class = NovoClienteSerializerConsulta
    lookup_field = 'id'

#Alteracao de status no banco de dados do campo AfiliadoCliente
class ClienteDetailViewAlteracao(UpdateAPIView):
    queryset = Processos.objects.all()
    serializer_class = ClienteSerializerAlteracao
    lookup_field = 'id'

#Alteracao de status no banco de dados do campo AdmAfiliado
class ClienteDetailViewAlteracaoStatusAdmAfiliado(UpdateAPIView):
    queryset = Processos.objects.all()
    serializer_class = ClienteSerializerAlteracaoAdmAfiliado
    lookup_field = 'id'

#Funcao para auxiliar na formatacao das datas antes de salvar
def formatar_data(data_string, formato_origem, formato_destino='%Y-%m-%d'):
    try:
        return datetime.strptime(data_string, formato_origem).strftime(formato_destino)
    except ValueError:
        return None
    
@api_view(['PATCH'])
def AtualizaClienteView(request, id):  # Adicionando cliente_id para identificar o registro
    try:
        cliente = Processos.objects.get(pk=id)  # Obtenha o cliente pelo ID
    except Processos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #obter o ClientJob e o FinanciamentoVeiculo associados, ou defina-os como None se eles não existirem
    client_job = ClientJob.objects.filter(processo=cliente).first()
    financiamento_veiculo = FinanciamentoVeiculo.objects.filter(processo=cliente).first()


    data = request.data.copy()
    #print(data)
    #Data de nascimento esta chegando no formato brasil, preciso ajustar antes de salvar
    data_nascimento = data.get('data_nascimento')
    if data_nascimento:
        data_formatada = formatar_data(data_nascimento[0] if isinstance(data_nascimento, list) else data_nascimento, '%d/%m/%Y')
        if data_formatada:
            data['data_nascimento'] = data_formatada
        else:
            return Response({'error': 'Formato inválido para data de nascimento.'}, status=status.HTTP_400_BAD_REQUEST)
            
    #Data de casamento esta chegando no formato brasil, preciso ajustar antes de salvar
    data_casamento = data.get('data casamento')
    if data_casamento:
        data_formatada = formatar_data(data_casamento[0] if isinstance(data_casamento, list) else data_casamento, '%d/%m/%Y')
        if data_formatada:
            data['data_casamento'] = data_formatada
        else:
            return Response({'error': 'Formato inválido para data de casamento.'}, status=status.HTTP_400_BAD_REQUEST)
    
    
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

    # Remover campos de documentos do data original para evitar problemas com o serializador
    for key in list(data.keys()):
        if key.startswith('documentos'):
            del data[key]

    data['documentos'] = documentos_data

    
    cliente_serializer = AtualizaClienteSerializer(cliente, data=data, partial=True)  
    if cliente_serializer.is_valid():
        cliente_serializer.validated_data['documentos'] = documentos_data
        cliente_serializer.save()
    else:
        return Response(cliente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # Atualize ou crie o ClientJob
    client_job_fields = client_job.get_field_names() if client_job else []
    #print(client_job_fields)
    #incluir um campo no client_job_data apenas se ele estiver presente na solicitação. Aqui está como você pode fazer isso:
    client_job_data = {
        field: data.get(field) for field in client_job_fields if field in data
    }
    if client_job_data:
        client_job_serializer = ClientJobSerializer(client_job, data=client_job_data, partial=True)
        if client_job_serializer.is_valid():
            client_job_serializer.save()
        else:
            return Response(client_job_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    financiamento_veiculo_fields = financiamento_veiculo.get_field_names() if financiamento_veiculo else []
    # Atualize ou crie o FinanciamentoVeiculo
    financiamento_veiculo_data = {
        field: data.get(field) for field in financiamento_veiculo_fields if field in data
    }
    #print(financiamento_veiculo_data)
    if financiamento_veiculo_data:
        financiamento_veiculo_serializer = FinanciamentoVeiculoSerializer(financiamento_veiculo, data=financiamento_veiculo_data, partial=True)
        if financiamento_veiculo_serializer.is_valid():
            financiamento_veiculo_serializer.save()
        else:
            return Response(financiamento_veiculo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(cliente_serializer.data, status=status.HTTP_200_OK)


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
    serializer_class = ClienteSerializerConsulta  # ou o serializer apropriado

    def get_queryset(self):
        """
        Este método irá retornar uma lista de pedidos para o funcionário especificado.
        O funcionário é determinado pelo `id` passado na URL.
        """
        funcionario_id = self.kwargs['funcionario_id']
        return Processos.objects.filter(funcionario__id=funcionario_id)  

class PedidosPorClienteListView(generics.ListAPIView):
    serializer_class = ClienteSerializerConsulta

    def get_queryset(self):
        """
        Este método irá retornar uma lista de pedidos para o afiliado especificado.
        O afiliado é determinado pelo `id` passado na URL.
        """
        cliente_id = self.kwargs['idCliente']
        return Processos.objects.filter(idCliente=cliente_id)
    
@api_view(['DELETE'])
def delete_documento_api(request, documento_id):
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
def criar_cliente_com_relacionados(request):
    logger.info("Iniciando a criação do cliente e relacionados...")
    data = request.data.copy()  # Mudança aqui

    # Chamada para a função que cria ou atualiza o cliente
    try:
        cliente_data, is_new = criar_ou_atualizar_cliente(data)
    except Exception as e:
        logger.error(f"Erro ao criar ou atualizar cliente: {str(e)}")
        print(e)
        return Response({"error": "Erro ao criar ou atualizar cliente."}, status=status.HTTP_400_BAD_REQUEST)


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
    processo_serializer.validated_data['idCliente'] = cliente_data['id']  # ou cliente_data.id se for um objeto
    processo_obj = processo_serializer.save() # Aqui você obtém o objeto Processos criado


    # Chamada para a funcao para criar os dados do cartorio caso tenha essa informacao
    cartorio_data_fields = Cartorio.get_field_names()
    cartorio_data = {}
    for field in cartorio_data_fields:
        cartorio_data[field] = data.get(f'cartorio[{field}]', None)
    print(cartorio_data)
    if cartorio_data and not all(value is None for value in cartorio_data.values()):
        try:
            criar_cartorio(cartorio_data, processo_obj)
        except ValueError as e:
            logger.error(f"Erro na criação do cartorio: {str(e)}")
            print(f"Erro na criação do cartorio: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Chamada para a funcao para criar os dados do cliente terceiro caso tenha essa informacao
    cliente_terceiro_data_fields = ClienteTerceiro.get_field_names()
    cliente_terceiro_data = {}
    for field in cliente_terceiro_data_fields:
        cliente_terceiro_data[field] = data.get(f'cliente_terceiro[{field}]', None)
    print(cliente_terceiro_data)
    if cliente_terceiro_data and not all(value is None for value in cliente_terceiro_data.values()):
        try:
            criar_cliente_terceiro(cliente_terceiro_data, processo_obj)
        except ValueError as e:
            logger.error(f"Erro na criação do cliente_terceiro: {str(e)}")
            print(f"Erro na criação do cliente_terceiro: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
    # Chamada para a funcao para criar os dados das certidoes caso tenha essa informacao
    certidoes_data_fields = Certidoes.get_field_names()
    certidoes_data = {}
    for field in certidoes_data_fields:
        certidoes_data[field] = data.get(f'certidoes[{field}]', None)
    print(certidoes_data)
    if certidoes_data and not all(value is None for value in certidoes_data.values()):
        try:
            criar_certidoes(certidoes_data, processo_obj)
        except ValueError as e:
            logger.error(f"Erro na criação do certidoes: {str(e)}")
            print(f"Erro na criação do certidoes: {str(e)}")
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
def ClienteFinanciamentoVeiculo(request):
    logger.info("Iniciando a criação do cliente e relacionados...")
    data = request.data.copy()  # Mudança aqui

     # Chamada para a função que cria ou atualiza o cliente
    try:
        cliente_data, is_new = criar_ou_atualizar_cliente(data)
    except Exception as e:
        logger.error(f"Erro ao criar ou atualizar cliente: {str(e)}")
        return Response({"error": "Erro ao criar ou atualizar cliente."}, status=status.HTTP_400_BAD_REQUEST)
    
    
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
    processo_serializer.validated_data['idCliente'] = cliente_data['id']  # ou cliente_data.id se for um objeto
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
