# apps/invitations/views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
from functools import wraps
import json
import logging

from .models import TestInvitation, InvitationEvent
from .serializers import (
    CreateInvitationSerializer, AcceptInvitationSerializer,
    InvitationSerializer, InvitationResponseSerializer
)

logger = logging.getLogger(__name__)

# Decoradores de autenticación
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'user') or not request.user or not request.user.is_authenticated:
            return JsonResponse({'error': 'usuario no autenticado'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'user') or not request.user or not request.user.is_authenticated:
            return JsonResponse({'error': 'usuario no autenticado'}, status=401)
        if request.user.role != 'admin':
            return JsonResponse({'error': 'Acceso denegado. Se requieren privilegios de administrador'}, status=403)
        return view_func(request, *args, **kwargs)
    return wrapper

# Funciones auxiliares
def authenticate_user(response, user, is_guest=False):
    """Configura la cookie de autenticación para el usuario"""
    from ..accounts.views import set_auth_cookie  # Función auxiliar
    return set_auth_cookie(response, user, is_guest)

def transfer_guest_results(guest_user_id, new_user_id, test_id):
    """Transfiere resultados de guest a usuario regular"""
    from apps.results.models import Result  # Importación diferida
    
    updated = Result.objects.filter(
        user_id=guest_user_id,
        test_id=test_id
    ).update(user_id=new_user_id)
    
    # Verificar si el guest user ya no tiene resultados
    remaining_results = Result.objects.filter(user_id=guest_user_id).count()
    
    if remaining_results == 0:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        User.objects.filter(id=guest_user_id).delete()
    
    return updated

def create_guest_user():
    """Crea un usuario guest temporal"""
    from django.contrib.auth import get_user_model
    from django.contrib.auth.hashers import make_password
    import secrets
    from datetime import datetime
    
    User = get_user_model()
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    username = f"guest_{timestamp}_{secrets.token_hex(4)}"
    temp_password = secrets.token_hex(8)
    
    guest_user = User.objects.create(
        username=username,
        email=f"{username}@guest.temp",
        password=make_password(temp_password),
        first_name="Invitado",
        role="guest",
        birth_date=timezone.now().date().replace(year=timezone.now().year - 18)
    )
    
    return guest_user

def log_invitation_event(invitation, event_type, user=None, metadata=None):
    """Registra un evento de invitación"""
    InvitationEvent.objects.create(
        invitation=invitation,
        event_type=event_type,
        user=user,
        metadata=metadata or {}
    )


# Vistas Públicas
@csrf_exempt
@require_http_methods(["POST"])
@login_required
def create_invitation(request):
    """Crea una nueva invitación a un test"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    serializer = CreateInvitationSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse({'error': serializer.errors}, status=400)
    
    test_id = serializer.validated_data['test_id']
    message = serializer.validated_data.get('message', '')
    
    from apps.tests.models import Test
    try:
        test = Test.objects.get(id=test_id, is_active=True)
    except Test.DoesNotExist:
        return JsonResponse({'error': 'test no encontrado'}, status=404)
    
    # Crear invitación
    invitation = TestInvitation.objects.create(
        test=test,
        invited_by=request.user,
        message=message
    )
    
    log_invitation_event(invitation, 'created', request.user)
    
    # Generar URL
    invitation_url = invitation.invitation_url
    
    return JsonResponse({
        'invitation': InvitationSerializer(invitation).data,
        'invitation_url': invitation_url,
        'message': 'Invitación creada exitosamente'
    }, status=201)


@require_http_methods(["GET"])
def check_invitation(request):
    """Verifica el estado de una invitación"""
    token = request.GET.get('token')
    
    if not token:
        return JsonResponse({'error': 'token de invitación requerido'}, status=400)
    
    try:
        invitation = TestInvitation.objects.select_related(
            'test', 'invited_by', 'guest_user'
        ).get(token=token, expires_at__gt=timezone.now())
    except TestInvitation.DoesNotExist:
        return JsonResponse({'error': 'invitación no válida o expirada'}, status=404)
    
    # Registrar evento de visualización
    log_invitation_event(invitation, 'viewed', request.user if request.user.is_authenticated else None)
    
    # Construir respuesta
    response_data = InvitationResponseSerializer(invitation).data
    
    # Buscar resultados existentes
    current_user_id = request.user.id if request.user.is_authenticated else 0
    
    # Determinar para qué usuario buscar resultados
    if invitation.guest_user:
        result_user_id = invitation.guest_user.id
    elif current_user_id > 0:
        result_user_id = current_user_id
    else:
        result_user_id = None
    
    if result_user_id:
        from apps.results.models import Result
        # Buscar resultados en progreso o completados
        existing_result = Result.objects.filter(
            user_id=result_user_id,
            test_id=invitation.test.id
        ).order_by('-updated_at').first()
        
        if existing_result:
            response_data['result'] = {
                'id': existing_result.id,
                'status': existing_result.status,
                'score': existing_result.score,
                'started_at': existing_result.started_at,
                'completed_at': existing_result.completed_at,
                'updated_at': existing_result.updated_at
            }
    
    response_data['is_authenticated'] = request.user.is_authenticated
    response_data['current_user_id'] = current_user_id
    
    return JsonResponse(response_data)


@csrf_exempt
@require_http_methods(["POST"])
def accept_invitation(request):
    """Acepta una invitación"""
    token = request.GET.get('token')
    
    if not token:
        return JsonResponse({'error': 'token de invitación requerido'}, status=400)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = {}
    
    serializer = AcceptInvitationSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse({'error': serializer.errors}, status=400)
    
    as_guest = serializer.validated_data.get('as_guest', False)
    
    # Buscar invitación
    try:
        invitation = TestInvitation.objects.select_related(
            'test', 'invited_by', 'guest_user'
        ).get(token=token, expires_at__gt=timezone.now())
    except TestInvitation.DoesNotExist:
        return JsonResponse({'error': 'invitación no válida o expirada'}, status=404)
    
    current_user = request.user if request.user.is_authenticated else None
    current_user_id = current_user.id if current_user else 0
    
    response_data = {
        'test_id': invitation.test.id,
        'invitation_id': invitation.id
    }
    
    # Caso A: Ya hay guest_user asignado
    if invitation.guest_user:
        guest_user_id = invitation.guest_user.id
        
        # Subcaso A1: Usuario autenticado es el mismo guest
        if current_user_id == guest_user_id:
            invitation.is_used = True
            if invitation.is_guest and current_user.role == 'user':
                invitation.is_guest = False
            invitation.save()
            
            log_invitation_event(invitation, 'accepted', current_user)
            
            response_data.update({
                'user_id': current_user_id,
                'is_guest': invitation.is_guest,
                'message': 'Continuando con tu usuario'
            })
        
        # Subcaso A2: Usuario autenticado como "user" diferente
        elif current_user and current_user.role == 'user' and current_user_id != guest_user_id:
            with transaction.atomic():
                # Transferir resultados
                transferred = transfer_guest_results(guest_user_id, current_user_id, invitation.test.id)
                
                # Actualizar invitación
                invitation.guest_user = current_user
                invitation.is_guest = (current_user.role == 'guest')
                invitation.is_used = True
                invitation.save()
                
                log_invitation_event(invitation, 'accepted', current_user, {
                    'transferred_from_guest': guest_user_id,
                    'results_transferred': transferred
                })
            
            response_data.update({
                'user_id': current_user_id,
                'is_guest': invitation.is_guest,
                'transferred_from_guest': True,
                'message': 'Test asignado a tu cuenta'
            })
        
        # Subcaso A3: No autenticado - Autenticar automáticamente al guest
        else:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            try:
                guest_user = User.objects.get(id=guest_user_id)
                
                # Autenticar usuario guest (requiere configuración de sesión)
                from django.contrib.auth import login
                login(request, guest_user)
                
                invitation.is_used = True
                invitation.save()
                
                log_invitation_event(invitation, 'accepted', guest_user, {'auto_authenticated': True})
                
                response_data.update({
                    'user_id': guest_user_id,
                    'is_guest': invitation.is_guest,
                    'auto_authenticated': True,
                    'message': 'Autenticado automáticamente como usuario invitado'
                })
            except User.DoesNotExist:
                return JsonResponse({
                    'error': 'Usuario guest no encontrado',
                    'requires_login': True
                }, status=404)
    
    # Caso B: No hay guest_user asignado
    else:
        # Subcaso B1: Usuario autenticado
        if current_user:
            with transaction.atomic():
                invitation.guest_user = current_user
                invitation.is_guest = (current_user.role == 'guest')
                invitation.is_used = True
                invitation.save()
                
                log_invitation_event(invitation, 'accepted', current_user)
            
            response_data.update({
                'user_id': current_user_id,
                'is_guest': invitation.is_guest,
                'message': 'Test asignado a tu cuenta'
            })
        
        # Subcaso B2: Crear guest (solo si as_guest=True)
        elif as_guest:
            with transaction.atomic():
                guest_user = create_guest_user()
                
                invitation.guest_user = guest_user
                invitation.is_guest = True
                invitation.is_used = True
                invitation.save()
                
                log_invitation_event(invitation, 'accepted', guest_user, {'created_as_guest': True})
                
                # Autenticar al guest
                from django.contrib.auth import login
                login(request, guest_user)
            
            response_data.update({
                'user_id': guest_user.id,
                'is_guest': True,
                'auto_authenticated': True,
                'message': 'Cuenta de invitado creada'
            })
        
        # Subcaso B3: Requiere login
        else:
            return JsonResponse({
                'error': 'Inicia sesión para aceptar la invitación',
                'requires_login': True
            }, status=401)
    
    return JsonResponse(response_data)

@require_http_methods(["GET"])
@login_required
def get_user_invitations(request):
    """Obtiene las invitaciones creadas por el usuario"""
    invitations = TestInvitation.objects.select_related(
        'test', 'invited_by', 'guest_user'
    ).filter(invited_by=request.user).order_by('-created_at')
    
    return JsonResponse({
        'invitations': InvitationSerializer(invitations, many=True).data
    })

