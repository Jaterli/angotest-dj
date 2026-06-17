# apps/accounts/middleware.py
from django.contrib.auth.models import AnonymousUser

class JWTCookieMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ✅ Siempre partir de AnonymousUser, nunca None
        request.user = AnonymousUser()
        
        auth_header = request.headers.get('Authorization', '')
        token = None
        
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
        else:
            token = request.COOKIES.get('auth_token')
        
        if token:
            from .views import get_user_from_token
            user = get_user_from_token(token)
            if user and user.is_active:
                request.user = user
        
        return self.get_response(request)