# users/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .services import DataService, MIN_TESTS_FOR_RANKING
import logging
from functools import wraps

logger = logging.getLogger(__name__)


from django.db.models import Min
from .services import DataService, MIN_TESTS_FOR_RANKING, PREDEFINED_LEVELS


# Decorador para verificar autenticación
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'usuario no autenticado'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

# ====== Dashboard y Rankings ======

@require_http_methods(["GET"])
@login_required
def get_dashboard_data(request):
    """Obtiene datos del dashboard del usuario"""
    
    user_id = request.user.id
    data_service = DataService()
    
    # Obtener datos en paralelo (simulando concurrencia)
    personal_data = data_service.get_personal_data(user_id)
    level_data = data_service.get_personal_level_data(user_id)
    total_active_users = data_service.get_active_users_count()
    
    response = {
        'personal_data': personal_data,
        'level_data': level_data,
        'total_active_users': total_active_users
    }
    
    return JsonResponse(response)

@require_http_methods(["GET"])
@login_required
def get_rankings(request):
    """Obtiene rankings y posición del usuario"""
    
    user_id = request.user.id
    limit = int(request.GET.get('limit', 10))
    
    # Validar límite
    if limit < 1 or limit > 50:
        limit = 10
    
    data_service = DataService()
    
    # Inicializar respuesta
    response = {
        'top_by_tests': [],
        'top_by_avg_time_taken_per_question': {
            'all_attempts': [],
            'first_attempt': []
        },
        'top_by_accuracy': {
            'all_attempts': [],
            'first_attempt': []
        },
        'top_by_questions_answered': {
            'all_attempts': [],
            'first_attempt': []
        },
        'top_by_levels': {},
        'top_by_levels_accuracy': {},
        'current_user_position': {
            'completed_tests': 0,
            'all_attempts': {
                'avg_time_taken_per_question': 0,
                'accuracy': 0,
                'questions_answered': 0
            },
            'first_attempt': {
                'avg_time_taken_per_question': 0,
                'accuracy': 0,
                'questions_answered': 0
            },
            'levels': {},
            'total_active_users': 0
        },
        'community_averages': {
            'all_attempts': {
                'avg_time_taken_per_question': 0,
                'avg_accuracy': 0,
                'avg_questions_per_user': 0
            },
            'first_attempt': {
                'avg_time_taken_per_question': 0,
                'avg_accuracy': 0,
                'avg_questions_per_user': 0
            },
            'levels': {}
        },
        'min_tests_for_ranking': MIN_TESTS_FOR_RANKING
    }
    
    # Obtener tops
    response['top_by_tests'] = data_service.get_top_by_metric('top_by_tests', limit)
    
    response['top_by_avg_time_taken_per_question']['all_attempts'] = data_service.get_top_by_avg_time('all', limit)
    response['top_by_avg_time_taken_per_question']['first_attempt'] = data_service.get_top_by_avg_time('first', limit)
    
    response['top_by_accuracy']['all_attempts'] = data_service.get_top_by_accuracy('all', limit)
    response['top_by_accuracy']['first_attempt'] = data_service.get_top_by_accuracy('first', limit)
    
    response['top_by_questions_answered']['all_attempts'] = data_service.get_top_by_questions_answered('all', limit)
    response['top_by_questions_answered']['first_attempt'] = data_service.get_top_by_questions_answered('first', limit)
    
    # Obtener rankings por niveles
    for level in PREDEFINED_LEVELS:
        response['top_by_levels'][level] = data_service.get_top_by_metric('top_by_level', limit, level)
        response['top_by_levels_accuracy'][level] = data_service.get_top_by_metric('top_by_levels_accuracy', limit, level)
    
    # Obtener posición del usuario
    response['current_user_position'] = data_service.get_user_all_ranking_positions(user_id)
    
    # Obtener promedios de comunidad
    response['community_averages'] = data_service.get_community_averages()
    
    return JsonResponse(response)