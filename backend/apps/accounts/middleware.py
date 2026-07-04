# apps/accounts/middleware.py
# Este Middleware es necesario cuando utilizamos usuarios personalizados en vez los predeterminados de Django
import logging
from django.contrib.auth.models import AnonymousUser

logger = logging.getLogger(__name__)

class JWTCookieMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # PRIMERO: Verificar si es admin ANTES de hacer cualquier cosa
        if request.path_info.startswith('/django-admin/'):
            # NO tocar request.user, NO hacer nada
            return self.get_response(request)
               
        # Guardar referencia al usuario original por si acaso
        original_user = request.user
        
        try:
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
                    logger.info(f"JWT User set: {user.email}")
                else:
                    # Si el token es inválido, usar AnonymousUser
                    request.user = AnonymousUser()
                    logger.error(f"JWT invalid, using AnonymousUser")
            else:
                # Sin token, mantener el usuario original o AnonymousUser
                if not original_user or isinstance(original_user, AnonymousUser):
                    request.user = AnonymousUser()
                else:
                    request.user = original_user
                    
        except Exception as e:
            logger.error(f"Error in JWTCookieMiddleware: {e}")
            # En caso de error, mantener el usuario original
            request.user = original_user
        
        return self.get_response(request)