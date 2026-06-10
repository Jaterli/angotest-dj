# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
import json
import jwt
import secrets
import logging

from .models import User, PasswordResetToken
from .serializers import UserResponseSerializer

logger = logging.getLogger(__name__)

def generate_jwt_token(user, is_guest=False):
    """Genera un token JWT para el usuario"""
    secret = settings.JWT_SECRET
    if not secret:
        raise ValueError("JWT_SECRET no configurado en el entorno")
    
    payload = {
        'user_id': user.id,
        'role': user.role,
        'is_guest': is_guest,
        'exp': timezone.now() + timedelta(hours=24),
        'iat': timezone.now(),
    }
    
    token = jwt.encode(payload, secret, algorithm='HS256')
    return token

def set_auth_cookie(response, user, is_guest=False):
    """Configura la cookie de autenticación"""
    try:
        token = generate_jwt_token(user, is_guest)
        
        # Actualizar login_at
        user.login_at = timezone.now()
        user.save(update_fields=['login_at'])
        
        # Configuración de la cookie
        is_production = getattr(settings, 'ENV', 'development') == 'production'
        
        response.set_cookie(
            'auth_token',
            token,
            max_age=24 * 60 * 60,  # 24 horas
            path='/',
            domain=None,
            secure=is_production,
            httponly=True,
            samesite='Strict' if is_production else 'Lax'
        )
        
        logger.info(f"Setting auth cookie | secure={is_production} | env={settings.ENV}")
        
    except Exception as e:
        logger.error(f"Error setting auth cookie: {str(e)}")
        raise

def get_user_from_token(token):
    """Obtiene el usuario a partir del token JWT"""
    try:
        secret = settings.JWT_SECRET
        if not secret:
            return None
        
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        user_id = payload.get('user_id')
        
        if not user_id:
            return None
        
        return User.objects.filter(id=user_id).first()
        
    except jwt.InvalidTokenError:
        return None

def authenticate_middleware(get_response):
    """Middleware para autenticar usuario a partir de la cookie"""
    def middleware(request):
        token = request.COOKIES.get('auth_token')
        if token:
            user = get_user_from_token(token)
            if user:
                request.user = user
            else:
                request.user = None
        else:
            request.user = None
        
        return get_response(request)
    return middleware


@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    """Registro de nuevos usuarios"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Validaciones
    required_fields = ['username', 'email', 'password', 'country', 'birth_date']
    for field in required_fields:
        if field not in data:
            return JsonResponse({'error': f'{field} is required'}, status=400)
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    country = data.get('country', '').strip()
    birth_date_str = data.get('birth_date', '')
    
    # Validaciones de longitud
    if len(username) < 3:
        return JsonResponse({'error': 'username must be at least 3 characters'}, status=400)
    if len(password) < 6:
        return JsonResponse({'error': 'password must be at least 6 characters'}, status=400)
    if not country:
        return JsonResponse({'error': 'country is required'}, status=400)
    
    # Validar formato de email
    if '@' not in email or '.' not in email:
        return JsonResponse({'error': 'invalid email format'}, status=400)
    
    # Verificar si el usuario ya existe
    if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'email or username already registered'}, status=400)
    
    # Parsear fecha de nacimiento
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'invalid date format. Use YYYY-MM-DD'}, status=400)
    
    # Crear usuario
    user = User(
        username=username,
        email=email,
        password=make_password(password),
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        phone=data.get('phone', ''),
        address=data.get('address', ''),
        country=country,
        birth_date=birth_date,
        role=data.get('role', 'user')
    )
    
    try:
        user.save()
        
        # Serializar respuesta
        serializer = UserResponseSerializer(user)
        
        return JsonResponse({'user': serializer.data}, status=201)
        
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return JsonResponse({'error': 'error creating user'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """Login de usuarios - retorna JWT en JSON y cookie"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    email = data.get('email', '')
    password = data.get('password', '')
    
    if not email or not password:
        return JsonResponse({'error': 'email and password are required'}, status=400)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'error': 'invalid credentials'}, status=401)
    
    if not check_password(password, user.password):
        return JsonResponse({'error': 'invalid credentials'}, status=401)
    
    # Generar token JWT
    token = generate_jwt_token(user, False)
    
    # Crear respuesta con el token en JSON
    response = JsonResponse({
        'user': UserResponseSerializer(user).data,
        'message': 'Login exitoso',
        'access_token': token,  # Token para el frontend
        'token_type': 'Bearer'
    })
    
    # Opcional: mantener cookie para compatibilidad
    try:
        set_auth_cookie(response, user, False)
    except Exception as e:
        logger.error(f"Error setting auth cookie: {str(e)}")
    
    return response


@require_http_methods(["GET"])
def check_auth(request):
    """Verificar autenticación del usuario - soporta header y cookie"""
    # Primero intentar header Authorization
    auth_header = request.headers.get('Authorization', '')
    token = None
    
    if auth_header.startswith('Bearer '):
        token = auth_header[7:]
    else:
        # Fallback a cookie
        token = request.COOKIES.get('auth_token')
    
    if not token:
        return JsonResponse({'authenticated': False})
    
    user = get_user_from_token(token)
    
    if not user:
        return JsonResponse({'authenticated': False})
    
    return JsonResponse({
        'authenticated': True,
        'user': UserResponseSerializer(user).data
    })


@csrf_exempt
@require_http_methods(["POST"])
def logout(request):
    # Con JWT, el logout es solo frontend
    # Pero podemos eliminar la cookie si existe
    response = JsonResponse({'message': 'Sesión cerrada exitosamente'})
    response.delete_cookie('auth_token', path='/')
    return response


@require_http_methods(["GET"])
def get_current_user(request):
    """Obtener usuario actual autenticado"""
    if not hasattr(request, 'user') or not request.user:
        return JsonResponse({'error': 'Usuario no autenticado'}, status=401)
    
    return JsonResponse({
        'user': UserResponseSerializer(request.user).data
    })

@csrf_exempt
@require_http_methods(["POST"])
def forgot_password(request):
    """Solicitar recuperación de contraseña"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    email = data.get('email', '')
    
    if not email:
        return JsonResponse({'error': 'email is required'}, status=400)
    
    # Buscar usuario (sin revelar si existe)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({
            'message': 'Si el email existe, se ha enviado un enlace de recuperación'
        })
    
    # Generar token único
    token = secrets.token_hex(32)
    
    # Crear registro en BD
    reset_token = PasswordResetToken(
        user=user,
        token=token,
        used=False,
        expires_at=timezone.now() + timedelta(hours=24)
    )
    reset_token.save()
    
    # Construir link de recuperación
    reset_link = f"https://{request.get_host()}/reset-password?token={token}"
    
    logger.info(f"Password reset link for {user.email}: {reset_link}")
    
    # Enviar email
    try:
        send_password_reset_email(user.email, reset_link)
    except Exception as e:
        logger.error(f"Error sending password reset email: {str(e)}")
    
    return JsonResponse({
        'message': 'Si el email existe, se ha enviado un enlace de recuperación',
        'reset_link': reset_link  # Solo en desarrollo
    })

@csrf_exempt
@require_http_methods(["POST"])
def reset_password(request):
    """Restablecer contraseña con token"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    token = data.get('token', '')
    new_password = data.get('new_password', '')
    confirm_password = data.get('confirm_password', '')
    
    if not token or not new_password or not confirm_password:
        return JsonResponse({'error': 'token, new_password and confirm_password are required'}, status=400)
    
    # Validar contraseñas
    if new_password != confirm_password:
        return JsonResponse({'error': 'Las contraseñas no coinciden'}, status=400)
    
    if len(new_password) < 6:
        return JsonResponse({'error': 'password must be at least 6 characters'}, status=400)
    
    # Buscar token válido
    try:
        token_record = PasswordResetToken.objects.get(
            token=token,
            used=False,
            expires_at__gt=timezone.now()
        )
    except PasswordResetToken.DoesNotExist:
        return JsonResponse({'error': 'Token inválido o expirado'}, status=400)
    
    # Actualizar contraseña
    user = token_record.user
    user.password = make_password(new_password)
    user.save()
    
    # Marcar token como usado
    token_record.used = True
    token_record.save()
    
    return JsonResponse({'message': 'Contraseña actualizada exitosamente'})

@require_http_methods(["GET"])
def validate_reset_token(request):
    """Validar si un token es válido"""
    token = request.GET.get('token')
    
    if not token:
        return JsonResponse({'error': 'Token requerido'}, status=400)
    
    try:
        token_record = PasswordResetToken.objects.get(
            token=token,
            used=False,
            expires_at__gt=timezone.now()
        )
        return JsonResponse({'valid': True, 'message': 'Token válido'})
    except PasswordResetToken.DoesNotExist:
        return JsonResponse({'valid': False, 'error': 'Token inválido o expirado'}, status=400)

def send_password_reset_email(to_email, reset_link):
    """Envía email de recuperación de contraseña"""
    subject = 'Recuperación de contraseña'
    html_message = render_to_string('emails/password_reset.html', {
        'reset_link': reset_link,
        'expires_in': '24 horas'
    })
    plain_message = f"""
    Para restablecer tu contraseña, haz clic en el siguiente enlace:
    {reset_link}
    
    Este enlace expirará en 24 horas.
    
    Si no solicitaste este cambio, ignora este mensaje.
    """
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        html_message=html_message,
        fail_silently=False
    )