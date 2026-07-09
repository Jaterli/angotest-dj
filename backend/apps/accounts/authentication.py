# apps/accounts/authentication.py
from rest_framework.authentication import BaseAuthentication

class JWTCookieAuthentication(BaseAuthentication):
    def authenticate(self, request):
        from .views import get_user_from_token
        raw_token = request.COOKIES.get('auth_token')
        
        if not raw_token:
            return None
        
        user = get_user_from_token(raw_token)
        if user and user.is_active:
            return (user, None)
        return None
