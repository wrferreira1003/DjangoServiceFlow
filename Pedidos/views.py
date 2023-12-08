from rest_framework import status, generics
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ClientJobSerializer, FinanciamentoVeiculoSerializer, ClienteSerializerAlteracaoAdmAfiliado,NovoPedidoSerializer,DocumentoSerializer,ClienteSerializerConsulta,NovoClienteSerializerConsulta, ClienteSerializerAlteracao,AtualizaClienteSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Processos, Documento
from Cliente.models import Cliente
from Cliente.serializers import ClienteSerializer, ClienteExistenteSerializer
from Servicos.models import Servico
from financeiro.models import Transacao
from Afiliados.models import AfiliadosModel
from rest_framework.pagination import PageNumberPagination
import logging
from rest_framework.permissions import IsAuthenticated

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
        
        client_job_serializer.save(cliente=processo_obj)
        return client_job_serializer
    else:
        # Pode levantar uma exceção ou tratar o erro conforme a necessidade
        logger.error(f"Erro na validação dos documentos: {client_job_serializer.errors}")
        raise ValueError(f"Erro na validação do ClientJob: {client_job_serializer.errors}")

#Funcao que cria os Dados de financiamento do cliente
def criar_financiamento_veiculo(dados_financiamento, processo_obj):
    financiamento_serializer = FinanciamentoVeiculoSerializer(data=dados_financiamento)
    if financiamento_serializer.is_valid():
        financiamento_serializer.save(cliente=processo_obj)
        return financiamento_serializer
    else:
        # Pode levantar uma exceção ou tratar o erro conforme a necessidade
        print('Funcao financiamento veiculo',financiamento_serializer.errors)
        raise ValueError(f"Erro na validação do financiamentoVeiculo: {financiamento_serializer.errors}")

def extrair_subservico(subservico):
    # Já que subservico é uma string, não precisamos pegar o primeiro elemento de uma lista
    subservico_str = subservico.strip()

    # Dividimos a string pelo caractere '-' e removemos espaços em branco extras.
    partes = subservico_str.split('-')
    nome_subservico = partes[0].strip() if len(partes) > 0 else ''

    return nome_subservico

#----------------------------------------------------------------------------------------------#
@api_view(['POST'])
def criar_cliente_com_relacionados(request):
    logger.info("Iniciando a criação do cliente e relacionados...")
    try:
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
        

        # Chamada para a função que cria ou atualiza o cliente
        cliente_data, is_new = criar_ou_atualizar_cliente(data)
        if not cliente_data:
            logger.error("Erro ao criar ou atualizar cliente.")
            return Response({"error": "Erro ao criar ou atualizar cliente."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Vamos testar a validação dos documentos aqui
        doc_serializer = DocumentoSerializer(data=documentos_data, many=True)
        if doc_serializer.is_valid():
            logger.info("Documentos validados corretamente!")
        else:
            logger.error(f"Erro na validação dos documentos: {doc_serializer.errors}")

    
        processo_serializer = NovoPedidoSerializer(data=data)


        if processo_serializer.is_valid():
            processo_serializer.validated_data['documentos'] = documentos_data

            # Aqui você atualiza o validated_data com o ID do cliente antes de salvar o processo.
            processo_serializer.validated_data['idCliente'] = cliente_data['id']  # ou cliente_data.id se for um objeto

            processo_obj = processo_serializer.save()

            #Aqui vamos verificar se é financiamento de veiculo e se for criamos a instancia de financiamento e job
            subservico = request.data.get('subservico', '')
            nome_subservico = extrair_subservico(subservico)
            # Funcao que cria as instancias de job e financiamento.
            if nome_subservico == "Financiamento Veicular": 
                client_job = {
                    'profissao': data.get('client_job[profissao]', None),
                    'cargo': data.get('client_job[cargo]', None),
                    'renda_mensal': data.get('client_job[renda_mensal]', None),
                    'data_admissao': data.get('client_job[data_admissao]', None),
                    'telefone_trabalho': data.get('client_job[telefone_trabalho]', None),
                    'empresa': data.get('client_job[empresa]', None),
                    'cep_trabalho': data.get('client_job[cep_trabalho]', None),
                    'logradouro_trabalho': data.get('client_job[logradouro_trabalho]', None),
                    'complemento_trabalho': data.get('client_job[complemento_trabalho]', None),
                    'numero_trabalho': data.get('client_job[numero_trabalho]',None),
                    'bairro_trabalho': data.get('client_job[bairro_trabalho]', None),
                    'cidade_trabalho': data.get('client_job[cidade_trabalho]', None),
                    'estado_trabalho': data.get('client_job[estado_trabalho]', None),
                }
             
                # Compilando dados para financiamento_veiculo
                financiamento_veiculo = {
                    'tipo_veiculo': data.get('financiamento_veiculo[tipo_veiculo]', None),
                    'marca': data.get('financiamento_veiculo[marca]', None),
                    'modelo': data.get('financiamento_veiculo[modelo]', None),
                    'ano' : data.get('financiamento_veiculo[ano]', None),
                    'placa' : data.get('financiamento_veiculo[placa]', None),
                    'versao' : data.get('financiamento_veiculo[versao]', None),
                    'estado_licenciamento' : data.get('financiamento_veiculo[estado_licenciamento]', None),
                    'valor' : data.get('financiamento_veiculo[valor]', None),
                    'entrada' : data.get('financiamento_veiculo[entrada]', None),
                    'prazo' : data.get('financiamento_veiculo[prazo]', None),    
                    'banco' : data.get('financiamento_veiculo[banco]', None),
                }
            
            try:
                criar_client_job(client_job, processo_obj)
                criar_financiamento_veiculo(financiamento_veiculo, processo_obj)
            except ValueError as e:
                print(e)
                # Trate o erro conforme necessário
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) 
            
            # Agora, vamos criar a transação associada a esse cliente
            servico_id = data.get('servico')  #passa o id do serviço
            print(servico_id)

            transacao_obj = criar_transacao(cliente_data,processo_obj, servico_id,)

            if not transacao_obj:
                logger.error("Erro ao criar transação. Serviço não encontrado.")
                return Response({"error": "Serviço não encontrado."}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(processo_serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            logger.error(f"Erro no serializer: {processo_serializer.errors}")
            return Response(processo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        logger.exception(f"Erro inesperado na função criar_cliente_com_relacionados: {e}")
        return Response({"error": "Erro interno do servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    data = request.data.copy()
   
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

    cliente_serializer = AtualizaClienteSerializer(cliente, data=data, partial=True)  # Usando um serializer para atualização

    if cliente_serializer.is_valid():
        
        cliente_serializer.validated_data['documentos'] = documentos_data
   
        cliente_serializer.save()
        return Response(cliente_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(cliente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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