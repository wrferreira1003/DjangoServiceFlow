from rest_framework_simplejwt.tokens import TokenError, AccessToken
from rest_framework.response import Response
from rest_framework import status
from .models import AfiliadosModel

def check_token_last_login(view_func):
    def _decorator(request, *args, **kwargs):
        header = request.headers.get('Authorization')
        if not header:
            return Response({"error": "Token ausente."}, status=status.HTTP_401_UNAUTHORIZED)
        
        token_string = header.split(' ')[1]
        try:
            token = AccessToken(token_string)
            token_last_login = token['last_login_at']
            user_last_login = AfiliadosModel.objects.get(id=token['user_id']).last_login_at
            if token_last_login != str(user_last_login):
                return Response({"error": "Token inválido devido a re-login."}, status=status.HTTP_401_UNAUTHORIZED)
        except TokenError:
            return Response({"error": "Token inválido."}, status=status.HTTP_401_UNAUTHORIZED)

        return view_func(request, *args, **kwargs)

    return _decorator