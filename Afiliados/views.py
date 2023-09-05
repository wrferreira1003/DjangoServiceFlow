from .serializers import AfiliadosModelSerializer, AfiliadosPublicosSerializer, ChangePasswordSerializer
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
from datetime import timezone
from .decorators import check_token_last_login

class TodosAfiliadosViewSet(viewsets.ModelViewSet):  # ReadOnly porque só queremos listar, sem criar, atualizar ou deletar
    permission_classes = (IsAuthenticated,)
    queryset = AfiliadosModel.objects.all()
    serializer_class = AfiliadosModelSerializer

#Mostro os dados
class AfiliadosViewSet(viewsets.ModelViewSet):
    print("passou por aqui")
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
   
        
        # Se chegou aqui, as credenciais são válidas; gere o token
        refresh = RefreshToken.for_user(afiliado)
        access_token = str(refresh.access_token)

        # Serializar os dados do afiliado
        afiliado_data = AfiliadosModelSerializer(afiliado).data

        return Response({"token": access_token, "afiliado": afiliado_data}, status=status.HTTP_200_OK)
    
class AfiliadosPublicosView(ListAPIView):
    queryset = AfiliadosModel.objects.filter(user_type='AFILIADO')
    serializer_class = AfiliadosPublicosSerializer
    
