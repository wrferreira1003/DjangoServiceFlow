from .serializers import AfiliadosModelSerializer, AfiliadosPublicosSerializer, ChangePasswordSerializer, FuncionarioSerializerFuncionarios
from rest_framework import viewsets
from .models import AfiliadosModel
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
from urllib.parse import urlencode
from firebase_admin import auth
import uuid

link = 'https://rcfacil.cloud/api/'
src = 'https://rcfacil.cloud/static/logo.png'

#Funcao que gera um token unico para o cliente
def generate_validation_token():
    return uuid.uuid4().hex

#Funcao de email para o cliente
def send_validation_email(email, token):
    params = urlencode({'token': token})
    validation_url = f"{link}validate?{params}" #Ajustar em producao
    html_content = """
    <div style="text-align: center;">
        <img src="{src}" alt="Logo" style="max-width: 100px; margin-bottom: 20px;"><br>
        <h1>Valide seu e-mail para confirmar sua identidade.</h1>
        <p>Clique no botão abaixo para confirmar o seu endereço de e-mail.</p>
        <a href="{validation_url}" 
            style="background-color: #4CAF50; 
            border: none; color: white; 
            padding: 15px 32px; text-align: center; 
            text-decoration: none; display: 
            inline-block; font-size: 16px; margin: 
            4px 2px; cursor: pointer; border-radius: 12px;"
            >VALIDAR EMAIL
        </a>

            <p
            style=margin-top: 30px;
            >Essa mensagem foi enviada para 
            <a href="mailto:{email}">wrf.wellington@gmail.com</a>.
            </p>
    </div>
    """.format(validation_url=validation_url, email=email, link=link, src=src)

    send_mail(
        'Cadastro RCFácil - Validação de conta',
        f'{validation_url}',
        settings.DEFAULT_FROM_EMAIL,  
        [email],
        html_message=html_content,  # Definir mensagem HTML com o conteúdo formatado
    )

#Lista todos os Afiliados do Banco de dados
class TodosAfiliadosViewSet(viewsets.ModelViewSet):  # ReadOnly porque só queremos listar, sem criar, atualizar ou deletar
    #permission_classes = (IsAuthenticated,)
    serializer_class = AfiliadosModelSerializer

    def get_queryset(self):
        return AfiliadosModel.objects.filter(user_type='AFILIADO')
    
    def create(self, request, *args, **kwargs):
        try:
            return super(TodosAfiliadosViewSet, self).create(request, *args, **kwargs)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#Mostro os dados
class AfiliadosViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    queryset = AfiliadosModel.objects.all()
    serializer_class = AfiliadosModelSerializer
    
    def list(self, request, *args, **kwargs):
        try:
            # Pega o afiliado associado ao usuário autenticado
            afiliado = AfiliadosModel.objects.get(id=request.user.id)
        except AfiliadosModel.DoesNotExist:
            return Response({"detail": "Afiliado não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Serializa o afiliado
        serializer = self.get_serializer(afiliado)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def change_password(self, request, pk=None):
        afiliado = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')

            # Validando a senha atual
            if not check_password(old_password, afiliado.password):
                return Response({"detail": "Senha atual incorreta"}, status=status.HTTP_400_BAD_REQUEST)

            # Atualizando a senha
            afiliado.password = make_password(new_password)
            afiliado.save()

            return Response({"detail": "Senha atualizada com sucesso!"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegistrarAfiliadoView(APIView):
    def post(self, request):
        serializer = AfiliadosModelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        senha = request.data.get("senha")
   
        try:
            afiliado = AfiliadosModel.objects.get(email=email)
        except AfiliadosModel.DoesNotExist:
            return Response({"error": "Email inválido."}, status=status.HTTP_401_UNAUTHORIZED)
        

        if not afiliado.check_password(senha):
            return Response({"error": "Senha inválida."}, status=status.HTTP_401_UNAUTHORIZED)

        print(afiliado.id)    
        #Gerando o token do firebase
        firebase_token = auth.create_custom_token(str(afiliado.id))
        #print(firebase_token)
  

        # Se chegou aqui, as credenciais são válidas; gere o token
        refresh = RefreshToken.for_user(afiliado)
        access_token = str(refresh.access_token)

        # Serializar os dados do afiliado
        afiliado_data = AfiliadosModelSerializer(afiliado).data

        return Response({"token": access_token, "firebase_token": firebase_token, "afiliado": afiliado_data}, status=status.HTTP_200_OK)
    
class AfiliadosPublicosView(ListAPIView):
    serializer_class = AfiliadosPublicosSerializer
    def get_queryset(self):
        queryset = AfiliadosModel.objects.filter(user_type='AFILIADO')
        estado = self.kwargs.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset
    
class FuncionariosPorAfiliadoView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, afiliado_id):
        try:
            afiliado = AfiliadosModel.objects.get(id=afiliado_id)
            funcionarios = afiliado.funcionarios.filter(user_type='FUNC')
            serializer = FuncionarioSerializerFuncionarios(funcionarios, many=True)
            return Response(serializer.data)
        except AfiliadosModel.DoesNotExist:
            return Response({"error": "Afiliado não encontrado."}, status=status.HTTP_404_NOT_FOUND)

#Cadastro de Clientes no banco de dados
class ClientePorAfiliadoView(APIView):
    def post(self, request, afiliado_id):
        try:
            afiliado = AfiliadosModel.objects.get(id=afiliado_id)
            #cliente = afiliado.clientes.filter(user_type='CLIENTE')
            #serializer = AfiliadosModelSerializer(cliente, many=True)
        except AfiliadosModel.DoesNotExist:
            return Response({"error": "Afiliado não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()

        data['user_type'] = 'CLIENTE'
        data['afiliado_relacionado'] = afiliado.id
        
        #tokem de validação da conta
        validation_token = generate_validation_token()
        data['validation_token'] = validation_token
        
        serializer = AfiliadosModelSerializer(data=data)

        #tokem de validação da conta
        validation_token = generate_validation_token()
        data['validation_token'] = validation_token
        
        if serializer.is_valid():
            serializer.save()
            send_validation_email(data['email'], validation_token)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, afiliado_id):
        try:
            afiliado = AfiliadosModel.objects.get(id=afiliado_id)
        except AfiliadosModel.DoesNotExist:
            return Response({"error": "Cliente não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        
        serializer = AfiliadosModelSerializer(afiliado, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)