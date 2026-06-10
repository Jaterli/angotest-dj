# apps/accounts/middleware.py
from django.utils.deprecation import MiddlewareMixin
from .models import User

class JWTCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Importación diferida para evitar ciclo
        from .views import get_user_from_token
        
        # Primero intentar header Authorization
        auth_header = request.headers.get('Authorization', '')
        token = None
        
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
        else:
            # Fallback a cookie
            token = request.COOKIES.get('auth_token')
        
        if token:
            user = get_user_from_token(token)
            if user:
                request.user = user
        
        return self.get_response(request)