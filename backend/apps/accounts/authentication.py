# apps/accounts/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings

class JWTCookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Obtener token de la cookie
        raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        
        if raw_token is None:
            return None
        
        try:
            validated_token = AccessToken(raw_token)
            user = self.get_user(validated_token)
            return (user, validated_token)
        except Exception:
            return None

