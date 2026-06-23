# ai/views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from functools import wraps
import json
import time
import logging

from .services import (
    get_ai_provider, get_system_prompt, build_prompt,
    check_user_quota, generate_mock_test, make_ai_request,
    parse_ai_response, create_test_from_ai_response
)
from .models import AIRequestLog
from apps.admin_panel.models import SystemConfig, UserQuota
from apps.shared.models import get_level_choices

logger = logging.getLogger(__name__)

# Decorador para verificar autenticación
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Usuario no autenticado'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

# Constantes
VALID_QUESTION_OPTIONS = [10, 20, 30, 40, 50]
VALID_ANSWER_OPTIONS = [3, 4]

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def generate_ai_test(request):
    """Genera un test usando IA"""
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Validar campos
    generation_mode = data.get('generation_mode', 'guided')
    
    if generation_mode != 'prompt':
        # Modo guiado: validar temas
        required_fields = ['main_topic', 'sub_topic', 'specific_topic']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'error': f'{field} es obligatorio si no se usa ai_prompt'
                }, status=400)
    
    # Validar nivel
    level = data.get('level')
    valid_levels = get_level_choices()
    if level not in valid_levels:
        return JsonResponse({
            'error': 'Nivel no válido',
            'valid_levels': valid_levels
        }, status=400)
    
    # Validar número de preguntas
    num_questions = data.get('num_questions', 10)
    if num_questions not in VALID_QUESTION_OPTIONS:
        return JsonResponse({
            'error': 'Número de preguntas no válido',
            'valid_options': VALID_QUESTION_OPTIONS
        }, status=400)
    
    # Validar número de respuestas
    num_answers = data.get('num_answers', 4)
    if num_answers not in VALID_ANSWER_OPTIONS:
        return JsonResponse({
            'error': 'Número de respuestas no válido',
            'valid_options': VALID_ANSWER_OPTIONS
        }, status=400)
    
    user_id = request.user.id
    
    # Verificar quota
    has_quota, quota_data = check_user_quota(user_id)
    if not has_quota:
        return JsonResponse({
            'error': 'Has alcanzado el límite de tests generados para este mes',
            'code': 'QUOTA_EXCEEDED',
            'quota': quota_data
        }, status=403)
    
    # Preparar input para IA
    input_data = {
        'main_topic': data.get('main_topic', ''),
        'sub_topic': data.get('sub_topic', ''),
        'specific_topic': data.get('specific_topic', ''),
        'level': level,
        'num_questions': num_questions,
        'num_answers': num_answers,
        'language': data.get('language', 'es'),
        'generation_mode': generation_mode,
        'ai_prompt': data.get('ai_prompt', '')
    }
    
    # Obtener proveedor
    provider = get_ai_provider()
    
    # Crear log de solicitud
    ai_log = AIRequestLog.objects.create(
        user_id=user_id,
        main_topic=input_data['main_topic'],
        sub_topic=input_data['sub_topic'],
        specific_topic=input_data['specific_topic'],
        level=level,
        num_questions=num_questions,
        num_answers=num_answers,
        language=input_data['language'],
        generation_mode=generation_mode,
        ai_prompt=input_data['ai_prompt'],
        ai_provider=provider.name if provider else 'mock',
        ai_model=provider.model if provider else 'mock',
        status='pending'
    )
    
    try:
        start_time = time.time()
        
        if provider:
            # Usar IA
            prompt = build_prompt(input_data)
            messages = [
                {'role': 'system', 'content': get_system_prompt(provider.name)},
                {'role': 'user', 'content': prompt}
            ]
            
            payload = {
                'model': provider.model,
                'messages': messages,
                'temperature': provider.temperature,
                'max_tokens': provider.max_tokens,
                'stream': False
            }
            
            # Hacer solicitud
            result = make_ai_request(provider, payload)
            
            # Parsear respuesta
            ai_response = parse_ai_response(result, input_data)
            
            # Actualizar log
            ai_log.ai_response = result
            ai_log.response_time = time.time() - start_time
            ai_log.tokens_used = result.get('usage', {}).get('total_tokens', 0)
            
        else:
            # Usar mock
            ai_response = generate_mock_test(input_data)
            ai_log.ai_response = ai_response
        
        # Crear test en BD
        test = create_test_from_ai_response(ai_response, user_id, input_data)
        
        # Actualizar log
        ai_log.test = test
        ai_log.status = 'completed'
        ai_log.save()
        
        return JsonResponse({
            'message': 'Test generado exitosamente',
            'generated_test_id': test.pk,
            'test': {
                'id': test.pk,
                'title': test.title,
                'description': test.description,
                'main_topic': test.main_topic,
                'sub_topic': test.sub_topic,
                'specific_topic': test.specific_topic,
                'level': test.level,
                'questions_count': test.questions.count(),
            },
            'status': 'completed',
            'quota_used': True,
            'quota': quota_data
        })
        
    except Exception as e:
        ai_log.status = 'failed'
        ai_log.error_message = str(e)
        ai_log.save()
        
        logger.error(f"Error generating AI test: {str(e)}")
        
        return JsonResponse({
            'error': f'Error generando test: {str(e)}'
        }, status=500)

@require_http_methods(["GET"])
@login_required
def get_current_user_quota(request):
    """Obtiene la quota actual del usuario"""
    
    user_id = request.user.id
    month_year = timezone.now().strftime('%Y-%m')
    
    try:
        quota = UserQuota.objects.get(user_id=user_id, month_year=month_year)
    except UserQuota.DoesNotExist:
        max_requests = 5
        try:
            config = SystemConfig.objects.get(key='ai_requests_per_month')
            max_requests = int(config.value)
        except SystemConfig.DoesNotExist:
            pass
        
        quota = UserQuota.objects.create(
            user_id=user_id,
            month_year=month_year,
            max_requests=max_requests,
            used_requests=0
        )
    
    response = {
        'month_year': month_year,
        'max_requests': quota.max_requests,
        'used_requests': quota.used_requests,
        'remaining_requests': quota.max_requests - quota.used_requests,
        'percentage_used': (quota.used_requests / quota.max_requests * 100) if quota.max_requests > 0 else 0
    }
    
    return JsonResponse(response)

@require_http_methods(["GET"])
@login_required
def get_ai_request_logs(request):
    """Obtiene el historial de solicitudes de IA del usuario"""
    
    user_id = request.user.id
    limit = int(request.GET.get('limit', 20))
    
    logs = AIRequestLog.objects.filter(
        user_id=user_id
    ).select_related('test').order_by('-created_at')[:limit]
    
    logs_data = []
    for log in logs:
        logs_data.append({
            'id': log.pk,
            'test_id': log.test.id if log.test else None,
            'test_title': log.test.title if log.test else None,
            'level': log.level,
            'num_questions': log.num_questions,
            'num_answers': log.num_answers,
            'generation_mode': log.generation_mode,
            'status': log.status,
            'error_message': log.error_message,
            'response_time': log.response_time,
            'created_at': log.created_at.isoformat(),
        })
    
    return JsonResponse({
        'logs': logs_data,
        'total': len(logs_data)
    })

@require_http_methods(["GET"])
@login_required
def get_ai_request_detail(request, log_id):
    """Obtiene el detalle de una solicitud de IA"""
    
    user_id = request.user.id
    
    try:
        log = AIRequestLog.objects.select_related('test').get(id=log_id, user_id=user_id)
    except AIRequestLog.DoesNotExist:
        return JsonResponse({'error': 'Solicitud no encontrada'}, status=404)
    
    return JsonResponse({
        'id': log.pk,
        'test': {
            'id': log.test.id,
            'title': log.test.title,
            'description': log.test.description,
            'main_topic': log.test.main_topic,
            'sub_topic': log.test.sub_topic,
            'specific_topic': log.test.specific_topic,
            'level': log.test.level,
        } if log.test else None,
        'input': {
            'main_topic': log.main_topic,
            'sub_topic': log.sub_topic,
            'specific_topic': log.specific_topic,
            'level': log.level,
            'num_questions': log.num_questions,
            'num_answers': log.num_answers,
            'language': log.language,
            'generation_mode': log.generation_mode,
            'ai_prompt': log.ai_prompt,
        },
        'ai_provider': log.ai_provider,
        'ai_model': log.ai_model,
        'status': log.status,
        'error_message': log.error_message,
        'response_time': log.response_time,
        'tokens_used': log.tokens_used,
        'created_at': log.created_at.isoformat(),
        'updated_at': log.updated_at.isoformat(),
    })