# results/views.py
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.paginator import Paginator
from functools import wraps
import json
import logging
from django.db.models import Q, Sum, Count, Avg, F, Case, When, Value, FloatField, IntegerField
from django.db.models.functions import Coalesce, Round, Cast
from datetime import datetime, timedelta
from django.core.cache import cache

from apps.test.models import Question, Answer
from apps.accounts.models import User
from .models import Result
from apps.shared.models import get_main_topics, get_level_choices, get_status_choices

logger = logging.getLogger(__name__)

# Decorador para verificar autenticación
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'usuario no autenticado'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

# Decorador para verificar admin
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'No autenticado'}, status=401)
        
        if request.user.role != 'admin':
            logger.warning(f"Acceso denegado para usuario {request.user.id} con rol {request.user.role}")
            return JsonResponse({'error': 'Acceso denegado. Se requieren privilegios de administrador'}, status=403)
        
        logger.info(f"Acceso concedido para usuario {request.user.id} con rol {request.user.role}")
        return view_func(request, *args, **kwargs)
    return wrapper

# ====== Función auxiliar para obtener respuestas correctas de forma eficiente ======
def get_correct_answers_for_test(test_id):
    """Obtener todas las respuestas correctas de un test de una sola consulta"""
    cache_key = f'test_correct_answers_{test_id}'
    correct_answers = cache.get(cache_key)
    
    if correct_answers is None:
        answers = Answer.objects.filter(
            question__test_id=test_id,
            is_correct=True
        ).select_related('question').values('question_id', 'id', 'answer_text')
        
        correct_answers = {
            answer['question_id']: {'id': answer['id'], 'text': answer['answer_text']}
            for answer in answers
        }
        cache.set(cache_key, correct_answers, timeout=3600)  # Cache por 1 hora
    
    return correct_answers


# ====== Obtener respuestas incorrectas ======
@require_http_methods(["GET"])
@login_required
def get_incorrect_answers(request, result_id):
    """Obtener respuestas incorrectas de un resultado completado"""
    
    try:
        result = Result.objects.select_related('test').get(id=result_id, user_id=request.user.id)
    except Result.DoesNotExist:
        return JsonResponse({'error': 'resultado no encontrado'}, status=404)
    
    # Parsear respuestas del usuario
    user_answers = result.answers if isinstance(result.answers, dict) else (json.loads(result.answers) if result.answers else {})
    
    # Obtener respuestas correctas del test (usando caché)
    correct_answers_map = get_correct_answers_for_test(result.test_id)
    
    # Obtener preguntas con sus respuestas
    questions = Question.objects.filter(test_id=result.test_id).prefetch_related('answers')
    
    incorrect_questions = []
    for idx, question in enumerate(questions, 1):
        user_answer_id = user_answers.get(str(question.pk))
        correct_answer = correct_answers_map.get(question.pk)
        
        if user_answer_id != correct_answer['id'] if correct_answer else True:
            # Obtener texto de respuesta del usuario
            user_answer_text = 'No respondida'
            if user_answer_id:
                user_answer = Answer.objects.filter(id=user_answer_id).values_list('answer_text', flat=True).first()
                if user_answer:
                    user_answer_text = user_answer
            
            incorrect_questions.append({
                'question_id': question.pk,
                'question_number': idx,
                'question_text': question.question_text,
                'correct_answer_id': correct_answer['id'] if correct_answer else None,
                'correct_answer_text': correct_answer['text'] if correct_answer else 'No definida',
                'user_answer_text': user_answer_text
            })
    
    total_questions = result.correct_answers + result.wrong_answers
    score_percentage = (result.correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    return JsonResponse({
        'incorrect_questions': incorrect_questions,
        'summary': {
            'total_questions': total_questions,
            'total_correct': result.correct_answers,
            'total_incorrect': result.wrong_answers,
            'questions_with_errors': len(incorrect_questions),
            'score_percentage': round(score_percentage, 2)
        }
    })

# ====== Función auxiliar ======
def test_to_dict(test):
    """Convierte un objeto Test a diccionario con todas sus relaciones"""
    return {
        'id': test.id,
        'title': test.title,
        'description': test.description,
        'main_topic': test.main_topic,
        'sub_topic': test.sub_topic,
        'specific_topic': test.specific_topic,
        'level': test.level,
        'is_active': test.is_active,
        'created_by': test.created_by,
        'created_at': test.created_at.isoformat() if test.created_at else None,
        'updated_at': test.updated_at.isoformat() if test.updated_at else None,
        'questions': [
            {
                'id': q.id,
                'question_text': q.question_text,
                'answers': [
                    {
                        'id': a.id,
                        'answer_text': a.answer_text,
                        'is_correct': a.is_correct
                    }
                    for a in q.answers.all()
                ]
            }
            for q in test.questions.all()
        ]
    }

def format_time(seconds):
    """Formatea segundos a formato legible"""
    if seconds <= 0:
        return ''
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

# ====== Vistas de Resultados (Admin) ======

@require_http_methods(["GET"])
@admin_required
def get_result_stats(request):
    """Obtener estadísticas generales de resultados"""
    
    # Usar caché para estadísticas que no cambian frecuentemente
    cache_key = 'result_stats'
    stats_data = cache.get(cache_key)
    
    if stats_data is None:
        total_results = Result.objects.count()
        
        status_stats = list(Result.objects.values('status').annotate(count=Count('id')))
        
        # Estadísticas de completados
        completed_results = Result.objects.filter(status='completed')
        total_correct = completed_results.aggregate(total=Sum('correct_answers'))['total'] or 0
        total_answered = completed_results.aggregate(
            total=Sum(F('correct_answers') + F('wrong_answers'))
        )['total'] or 0
        avg_score = (total_correct / total_answered * 100) if total_answered > 0 else 0
        
        # Resultados por día (últimos 30 días)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        daily_stats = Result.objects.filter(
            started_at__gte=thirty_days_ago
        ).extra(
            {'day': "DATE(started_at)"}
        ).values('day').annotate(
            count=Count('id'),
            avg_score=Avg(
                Case(
                    When(status='completed', then=F('correct_answers') * 100.0 / (F('correct_answers') + F('wrong_answers'))),
                    default=Value(0.0),
                    output_field=FloatField()
                )
            )
        ).order_by('day')
        
        # Resultados por nivel de test
        level_stats = list(Result.objects.filter(status='completed').select_related('test').values('test__level').annotate(
            count=Count('id'),
            avg_score=Avg(F('correct_answers') * 100.0 / (F('correct_answers') + F('wrong_answers')))
        ))
        
        # Top 10 tests más realizados
        top_tests = list(Result.objects.select_related('test').values(
            'test__id', 'test__title'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:10])
        
        # Top 10 usuarios con más resultados
        top_users = list(Result.objects.select_related('user').values(
            'user__id', 'user__username', 'user__email'
        ).annotate(
            count=Count('id'),
            avg_score=Avg(
                Case(
                    When(status='completed', then=F('correct_answers') * 100.0 / (F('correct_answers') + F('wrong_answers'))),
                    default=Value(0.0),
                    output_field=FloatField()
                )
            )
        ).order_by('-count')[:10])
        
        stats_data = {
            'stats': {
                'total_results': total_results,
                'average_score': round(avg_score, 2),
                'by_status': status_stats,
                'by_level': level_stats,
                'daily_last_30_days': [
                    {
                        'date': item['day'].isoformat() if item['day'] else None,
                        'count': item['count'],
                        'avg_score': round(float(item['avg_score']), 2) if item['avg_score'] else 0
                    }
                    for item in daily_stats
                ],
                'top_tests': [
                    {
                        'test_id': item['test__id'],
                        'test_title': item['test__title'],
                        'times_taken': item['count']
                    }
                    for item in top_tests
                ],
                'top_users': [
                    {
                        'user_id': item['user__id'],
                        'username': item['user__username'],
                        'email': item['user__email'],
                        'results_count': item['count'],
                        'avg_score': round(float(item['avg_score']), 2) if item['avg_score'] else 0
                    }
                    for item in top_users
                ]
            },
            'timestamp': timezone.now().isoformat()
        }
        
        cache.set(cache_key, stats_data, timeout=300)  # Cache por 5 minutos
    
    return JsonResponse(stats_data)

@require_http_methods(["GET"])
@admin_required
def get_result_detail(request, result_id):
    """Obtener detalle completo de un resultado"""
    try:
        result = Result.objects.select_related('user', 'test').get(id=result_id)
    except Result.DoesNotExist:
        return JsonResponse({'error': 'Resultado no encontrado'}, status=404)
    
    total_answered = result.correct_answers + result.wrong_answers
    score = round((result.correct_answers * 100.0 / total_answered), 2) if result.status == 'completed' and total_answered > 0 else 0
    
    answers_data = result.answers if isinstance(result.answers, dict) else (json.loads(result.answers) if result.answers else None)
    
    return JsonResponse({
        'id': result.pk,
        'user_id': result.user_id,
        'test_id': result.test_id,
        'correct_answers': result.correct_answers,
        'wrong_answers': result.wrong_answers,
        'total_questions': total_answered,
        'score': score,
        'time_taken': result.time_taken,
        'status': result.status,
        'answers': answers_data,
        'started_at': result.started_at.isoformat() if result.started_at else None,
        'updated_at': result.updated_at.isoformat() if result.updated_at else None,
        'user': {
            'id': result.user.id,
            'username': result.user.username,
            'email': result.user.email,
            'first_name': result.user.first_name,
            'last_name': result.user.last_name,
            'role': result.user.role,
        },
        'test': {
            'id': result.test.id,
            'title': result.test.title,
            'description': result.test.description,
            'main_topic': result.test.main_topic,
            'sub_topic': result.test.sub_topic,
            'specific_topic': result.test.specific_topic,
            'level': result.test.level,
            'total_questions': result.test.questions.count(),
        }
    })


@require_http_methods(["GET"])
@admin_required
def export_results_csv(request):
    """Exportar resultados a CSV con filtros aplicados"""
    import csv
    
    # Obtener parámetros de filtro
    user_id = request.GET.get('user_id')
    user_role = request.GET.get('user_role')
    user_email = request.GET.get('user_email')
    user_username = request.GET.get('user_username')
    
    test_id = request.GET.get('test_id')
    test_title = request.GET.get('test_title')
    test_main_topic = request.GET.get('test_main_topic')
    test_sub_topic = request.GET.get('test_sub_topic')
    test_specific_topic = request.GET.get('test_specific_topic')
    test_level = request.GET.get('test_level')
    test_created_by = request.GET.get('test_created_by')
    
    status = request.GET.get('status')
    min_score = request.GET.get('min_score')
    max_score = request.GET.get('max_score')
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    search = request.GET.get('search')
    
    # Construir query con filtros
    query = Result.objects.select_related('user', 'test')
    
    # Filtros de usuario
    if user_id:
        try:
            query = query.filter(user_id=int(user_id))
        except ValueError:
            pass
    
    if user_role:
        query = query.filter(user__role=user_role)
    
    if user_email:
        query = query.filter(user__email__icontains=user_email)
    
    if user_username:
        query = query.filter(user__username__icontains=user_username)
    
    # Filtros de test
    if test_id:
        try:
            query = query.filter(test_id=int(test_id))
        except ValueError:
            pass
    
    if test_title:
        query = query.filter(test__title__icontains=test_title)
    
    if test_main_topic:
        query = query.filter(test__main_topic=test_main_topic)
    
    if test_sub_topic:
        query = query.filter(test__sub_topic=test_sub_topic)
    
    if test_specific_topic:
        query = query.filter(test__specific_topic=test_specific_topic)
    
    if test_level:
        query = query.filter(test__level=test_level)
    
    if test_created_by:
        try:
            query = query.filter(test__created_by=int(test_created_by))
        except ValueError:
            pass
    
    # Filtros de resultado
    if status and status != 'all':
        query = query.filter(status=status)
    
    # Filtros de puntuación (usando annotate)
    if min_score or max_score:
        from django.db.models import F, Case, When, Value, FloatField
        from django.db.models.functions import Coalesce, Round
        
        query = query.annotate(
            score=Case(
                When(
                    status='completed',
                    then=Coalesce(
                        Round(F('correct_answers') * 100.0 / (F('correct_answers') + F('wrong_answers')), 2),
                        Value(0.0)
                    )
                ),
                default=Value(0.0),
                output_field=FloatField()
            )
        )
        
        if min_score:
            try:
                min_val = float(min_score)
                query = query.filter(score__gte=min_val)
            except ValueError:
                pass
        
        if max_score:
            try:
                max_val = float(max_score)
                query = query.filter(score__lte=max_val)
            except ValueError:
                pass
    
    # Filtros de fecha
    if start_date:
        try:
            from datetime import datetime
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(started_at__date__gte=start)
        except ValueError:
            pass
    
    if end_date:
        try:
            from datetime import datetime
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(started_at__date__lte=end)
        except ValueError:
            pass
    
    # Búsqueda general
    if search:
        query = query.filter(
            Q(user__username__icontains=search) |
            Q(user__email__icontains=search) |
            Q(test__title__icontains=search) |
            Q(test__main_topic__icontains=search) |
            Q(test__sub_topic__icontains=search)
        )
    
    # Ordenar por fecha de actualización descendente (más recientes primero)
    query = query.order_by('-updated_at')
    
    # Crear respuesta CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="results_export.csv"'
    
    # Añadir BOM para UTF-8 (compatibilidad con Excel)
    response.write('\ufeff')
    
    writer = csv.writer(response)
    
    # Cabeceras
    writer.writerow([
        'ID', 'Usuario', 'Email', 'Test', 'Nivel', 'Tema Principal',
        'Subtema', 'Tema Específico', 'Correctas', 'Incorrectas', 
        'Total Respondidas', 'Puntuación (%)', 'Tiempo (seg)',
        'Estado', 'Fecha Inicio', 'Última Actualización'
    ])
    
    # Usar iterator para eficiencia con grandes conjuntos de datos
    for result in query.iterator(chunk_size=1000):
        total_answers = result.correct_answers + result.wrong_answers
        score = 0
        if result.status == 'completed' and total_answers > 0:
            score = round((result.correct_answers / total_answers) * 100, 2)
        
        writer.writerow([
            result.pk,
            result.user.username,
            result.user.email,
            result.test.title,
            result.test.level,
            result.test.main_topic,
            result.test.sub_topic,
            result.test.specific_topic,
            result.correct_answers,
            result.wrong_answers,
            total_answers,
            score,
            result.time_taken,
            result.status,
            result.started_at.isoformat() if result.started_at else '',
            result.updated_at.isoformat() if result.updated_at else '',
        ])
    
    return response


# ====== Admin: Obtener lista de resultados con filtros avanzados ======
@require_http_methods(["GET"])
@admin_required
def get_results_list(request):
    """Obtener lista de resultados con paginación, filtrado y ordenación"""
    
    page = max(1, int(request.GET.get('page', 1)))
    page_size = min(100, max(1, int(request.GET.get('page_size', 20))))
    sort_by = request.GET.get('sort_by', 'updated_at')
    sort_order = request.GET.get('sort_order', 'desc')
    
    # Construir query base
    results_query = Result.objects.select_related('user', 'test').annotate(
        score=Case(
            When(status='completed', then=Coalesce(
                Round(F('correct_answers') * 100.0 / (F('correct_answers') + F('wrong_answers')), 2),
                Value(0.0)
            )),
            default=Value(0.0),
            output_field=FloatField()
        ),
        total_questions=F('correct_answers') + F('wrong_answers')
    )
    
    # Aplicar filtros
    filters = {}
    
    # Filtros de usuario
    if user_id := request.GET.get('user_id'):
        try:
            filters['user_id'] = int(user_id)
        except ValueError:
            pass
    
    if user_role := request.GET.get('user_role'):
        filters['user__role'] = user_role
    
    if user_email := request.GET.get('user_email'):
        results_query = results_query.filter(user__email__icontains=user_email)
    
    if user_username := request.GET.get('user_username'):
        results_query = results_query.filter(user__username__icontains=user_username)
    
    # Filtros de test
    if test_id := request.GET.get('test_id'):
        try:
            filters['test_id'] = int(test_id)
        except ValueError:
            pass
    
    if test_title := request.GET.get('test_title'):
        results_query = results_query.filter(test__title__icontains=test_title)
    
    if test_main_topic := request.GET.get('test_main_topic'):
        filters['test__main_topic'] = test_main_topic
    
    if test_sub_topic := request.GET.get('test_sub_topic'):
        filters['test__sub_topic'] = test_sub_topic
    
    if test_specific_topic := request.GET.get('test_specific_topic'):
        filters['test__specific_topic'] = test_specific_topic
    
    if test_level := request.GET.get('test_level'):
        filters['test__level'] = test_level
    
    if test_created_by := request.GET.get('test_created_by'):
        try:
            filters['test__created_by'] = int(test_created_by)
        except ValueError:
            pass
    
    # Filtros de resultado
    if status := request.GET.get('status'):
        filters['status'] = status
    
    # Aplicar filtros de diccionario
    results_query = results_query.filter(**filters)
    
    # Filtros de puntuación
    if min_score := request.GET.get('min_score'):
        try:
            results_query = results_query.filter(score__gte=float(min_score))
        except ValueError:
            pass
    
    if max_score := request.GET.get('max_score'):
        try:
            results_query = results_query.filter(score__lte=float(max_score))
        except ValueError:
            pass
    
    # Filtros de fecha
    if start_date := request.GET.get('start_date'):
        try:
            results_query = results_query.filter(started_at__date__gte=datetime.strptime(start_date, '%Y-%m-%d').date())
        except ValueError:
            pass
    
    if end_date := request.GET.get('end_date'):
        try:
            results_query = results_query.filter(started_at__date__lte=datetime.strptime(end_date, '%Y-%m-%d').date())
        except ValueError:
            pass
    
    # Búsqueda general
    if search := request.GET.get('search'):
        results_query = results_query.filter(
            Q(user__username__icontains=search) |
            Q(user__email__icontains=search) |
            Q(test__title__icontains=search) |
            Q(test__main_topic__icontains=search) |
            Q(test__sub_topic__icontains=search)
        )
    
    total_results = Result.objects.count()
    total_filtered_results = results_query.count()
    
    # Aplicar ordenación
    valid_sort_fields = ['id', 'started_at', 'updated_at', 'time_taken', 'correct_answers', 'score']
    if sort_by not in valid_sort_fields:
        sort_by = 'updated_at'
    
    order_field = f'-{sort_by}' if sort_order == 'desc' else sort_by
    results_query = results_query.order_by(order_field)
    
    # Paginación
    offset = (page - 1) * page_size
    paginated_results = results_query[offset:offset + page_size]
    
    # Convertir a lista de diccionarios manualmente
    results_list = []
    for result in paginated_results:
        results_list.append({
            'id': result.pk,
            'user_id': result.user_id,
            'test_id': result.test_id,
            'correct_answers': result.correct_answers,
            'wrong_answers': result.wrong_answers,
            'total_questions': result.total_questions,
            'score': result.score,
            'time_taken': result.time_taken,
            'status': result.status,
            'answers': result.answers,
            'started_at': result.started_at.isoformat(),
            'updated_at': result.updated_at.isoformat(),
            'user_username': result.user.username,
            'user_email': result.user.email,
            'user_first_name': result.user.first_name,
            'user_last_name': result.user.last_name,
            'user_role': result.user.role,
            'test_title': result.test.title,
            'test_description': result.test.description,
            'test_main_topic': result.test.main_topic,
            'test_sub_topic': result.test.sub_topic,
            'test_specific_topic': result.test.specific_topic,
            'test_level': result.test.level,
        })
    
    return JsonResponse({
        'results': results_list,
        'filters_applied': request.GET.dict(),
        'available_filters': {
            'main_topics': get_main_topics(),
            'levels': get_level_choices(),
            'statuses': get_status_choices(),
            'roles': ['user', 'admin'],
        },
        'stats': {
            'total_results': total_results,
            'total_filtered_results': total_filtered_results,
        }
    })


# ====== Eliminar un resultado específico ======
@csrf_exempt
@require_http_methods(["DELETE"])
@admin_required
def delete_result(request, result_id):
    """Eliminar un resultado específico"""
    deleted, _ = Result.objects.filter(id=result_id).delete()
    if not deleted:
        return JsonResponse({'error': 'Resultado no encontrado'}, status=404)
    
    # Limpiar caché de estadísticas
    cache.delete('result_stats')
    
    return JsonResponse({'message': 'Resultado eliminado', 'id': result_id})

# ====== Eliminar múltiples resultados (Bulk Delete) ======
@csrf_exempt
@require_http_methods(["DELETE"])
@admin_required
def delete_results_bulk(request):
    """Eliminar múltiples resultados"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    ids = data.get('ids', [])
    if not ids or not isinstance(ids, list):
        return JsonResponse({'error': 'Se requiere una lista de IDs'}, status=400)
    
    try:
        ids = [int(id_val) for id_val in ids]
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Los IDs deben ser números enteros'}, status=400)
    
    deleted_count, _ = Result.objects.filter(id__in=ids).delete()
    
    # Limpiar caché de estadísticas
    cache.delete('result_stats')
    
    return JsonResponse({
        'message': f'{deleted_count} resultados eliminados',
        'deleted_count': deleted_count
    })

# ====== Resultados de Usuario (Admin) ======
@require_http_methods(["GET"])
@admin_required
def get_user_results(request, user_id):
    """Obtener resultados de tests de un usuario específico"""
    
    # ===== OBTENER USUARIO =====
    try:
        user = User.objects.only(
            'id', 'username', 'email', 'first_name', 'last_name', 'role', 'registered_at'
        ).get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'usuario no encontrado'}, status=404)
    
    # ===== PARÁMETROS DE CONSULTA =====
    page = max(1, int(request.GET.get('page', 1)))
    page_size = min(100, max(1, int(request.GET.get('page_size', 20))))
    status_filter = request.GET.get('status', '')
    sort_by = request.GET.get('sort_by', 'updated_at')
    sort_order = request.GET.get('sort_order', 'desc')
    search = request.GET.get('search', '')
    level = request.GET.get('level', '')
    main_topic = request.GET.get('main_topic', '')
    sub_topic = request.GET.get('sub_topic', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    
    # ===== CONSULTA BASE =====
    query = Result.objects.filter(user_id=user_id).select_related('test')
    
    # ===== APLICAR FILTROS =====
    if status_filter and status_filter != 'all':
        query = query.filter(status=status_filter)
    
    if level:
        query = query.filter(test__level=level)
    
    if main_topic:
        query = query.filter(test__main_topic=main_topic)
    
    if sub_topic:
        query = query.filter(test__sub_topic=sub_topic)
    
    if search:
        query = query.filter(
            Q(test__title__icontains=search) |
            Q(test__description__icontains=search)
        )
    
    if from_date:
        try:
            from_date_parsed = datetime.strptime(from_date, '%Y-%m-%d').date()
            query = query.filter(started_at__date__gte=from_date_parsed)
        except ValueError:
            pass
    
    if to_date:
        try:
            to_date_parsed = datetime.strptime(to_date, '%Y-%m-%d').date()
            next_day = to_date_parsed + timedelta(days=1)
            query = query.filter(started_at__date__lt=next_day)
        except ValueError:
            pass
    
    # ===== CONTAR TOTAL Y FILTRADO =====
    total_results = Result.objects.filter(user_id=user_id).count()
    total_filtered = query.count()
    
    # ===== ORDENAR Y PAGINAR =====
    sort_mapping = {
        'average_score': 'score_percentage',
        'title': 'test__title',
        'level': 'test__level',
        't_created_at': 'test__created_at',
        'time_taken': 'time_taken',
        'started_at': 'started_at',
        'updated_at': 'updated_at',
    }
    
    order_field = sort_mapping.get(sort_by, 'updated_at')
    
    if sort_by == 'average_score':
        # Ordenamiento especial para average_score
        results_list = list(query)
        results_list.sort(
            key=lambda x: x.score_percentage if x.status == 'completed' else 0,
            reverse=(sort_order == 'desc')
        )
        offset = (page - 1) * page_size
        paginated_results = results_list[offset:offset + page_size]
        total_pages = (len(results_list) + page_size - 1) // page_size if page_size > 0 else 1
    else:
        if sort_order == 'desc':
            order_field = f'-{order_field}'
        query = query.order_by(order_field)
        paginator = Paginator(query, page_size)
        page_obj = paginator.get_page(page)
        paginated_results = page_obj.object_list
        total_pages = paginator.num_pages
    
    # ===== PROCESAR RESULTADOS =====
    user_results = []
    for result in paginated_results:
        total_questions = result.test.questions.count()
        
        score = 0.0
        if total_questions > 0 and result.status == 'completed':
            score = (result.correct_answers / total_questions * 100)
            score = round(score * 10) / 10
        
        answered_count = 0
        if result.status == 'completed':
            answered_count = result.correct_answers + result.wrong_answers
        elif result.status == 'in_progress' and result.answers:
            answers = result.answers if isinstance(result.answers, dict) else (json.loads(result.answers) if result.answers else {})
            answered_count = len(answers)
        
        user_results.append({
            'id': result.pk,
            'test_id': result.test.id,
            'test_title': result.test.title,
            'test_description': result.test.description,
            'test_main_topic': result.test.main_topic,
            'test_sub_topic': result.test.sub_topic,
            'test_specific_topic': result.test.specific_topic,
            'test_level': result.test.level,
            'total_questions': total_questions,
            'correct_answers': result.correct_answers,
            'wrong_answers': result.wrong_answers,
            'score': score,
            'time_taken': result.time_taken,
            'status': result.status,
            'started_at': result.started_at.isoformat(),
            'updated_at': result.updated_at.isoformat(),
            'test_created_at': result.test.created_at.isoformat(),
            'answered_count': answered_count
        })
    
    # ===== ESTADÍSTICAS =====
    stats_query = Result.objects.filter(user_id=user_id)
    
    # Aplicar filtros de fecha a las estadísticas
    if from_date:
        try:
            from_date_parsed = datetime.strptime(from_date, '%Y-%m-%d').date()
            stats_query = stats_query.filter(started_at__date__gte=from_date_parsed)
        except ValueError:
            pass
    
    if to_date:
        try:
            to_date_parsed = datetime.strptime(to_date, '%Y-%m-%d').date()
            next_day = to_date_parsed + timedelta(days=1)
            stats_query = stats_query.filter(started_at__date__lt=next_day)
        except ValueError:
            pass
    
    if status_filter and status_filter != 'all':
        stats_query = stats_query.filter(status=status_filter)
    
    stats = stats_query.aggregate(
        completed_tests=Count('id', filter=Q(status='completed')),
        in_progress_tests=Count('id', filter=Q(status='in_progress')),
        total_time_spent=Coalesce(Sum('time_taken'), Value(0)),
        total_questions_answered=Coalesce(
            Sum(
                Case(
                    When(status='completed', then=F('correct_answers') + F('wrong_answers')),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ),
            Value(0)
        ),
        average_score=Coalesce(
            Avg(
                Case(
                    When(status='completed', then=F('correct_answers') * 100.0 / (F('correct_answers') + F('wrong_answers'))),
                    output_field=FloatField()
                )
            ),
            Value(0.0)
        ),
        total_correct_answers=Coalesce(
            Sum(
                Case(
                    When(status='completed', then=F('correct_answers')),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ),
            Value(0)
        )
    )
    
    # ===== FILTROS DISPONIBLES =====
    main_topics = list(
        Result.objects.filter(user_id=user_id)
        .exclude(test__main_topic='')
        .values_list('test__main_topic', flat=True)
        .distinct()
        .order_by('test__main_topic')
    )
    
    # ===== CONSTRUIR RESPUESTA =====
    return JsonResponse({
        'results': user_results,
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total_filtered': total_filtered,
            'total_pages': total_pages,
        },
        'filters_applied': {
            'status': status_filter,
            'level': level,
            'main_topic': main_topic,
            'sub_topic': sub_topic,
            'from_date': from_date,
            'to_date': to_date,
            'search': search,
            'sort_by': sort_by,
            'sort_order': sort_order,
        },
        'stats': {
            'total_results': total_results,
            'total_filtered_results': total_filtered,
            'completed_tests': stats['completed_tests'] or 0,
            'in_progress_tests': stats['in_progress_tests'] or 0,
            'average_score': stats['average_score'],
            'total_time_spent': stats['total_time_spent'] or 0,
            'total_questions_answered': stats['total_questions_answered'] or 0,
            'total_correct_answers': stats['total_correct_answers'] or 0,
        },
        'available_filters': {
            'main_topics': main_topics,
            'levels': get_level_choices(),
            'statuses': ['all', 'completed', 'in_progress'],
        },
        'user': {
            'id': user.pk,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'registered_at': user.registered_at.isoformat() if user.registered_at else None,
        }
    })


@require_http_methods(["GET"])
@admin_required
def get_user_result_details(request, result_id, user_id=None):
    """Obtener detalles específicos de un resultado"""
    
    target_user_id = user_id if user_id else request.user.id
    
    if user_id and request.user.id != int(user_id) and request.user.role != 'admin':
        return JsonResponse({'error': 'no autorizado'}, status=403)
    
    try:
        user = User.objects.only('id', 'username', 'email', 'first_name', 'last_name', 'role', 'registered_at').get(id=target_user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'usuario no encontrado'}, status=404)
    
    try:
        result = Result.objects.select_related('test').get(
            id=result_id,
            user_id=target_user_id
        )
    except Result.DoesNotExist:
        return JsonResponse({'error': 'resultado no encontrado'}, status=404)
    
    # Parsear respuestas del usuario
    user_answers = result.answers if isinstance(result.answers, dict) else (json.loads(result.answers) if result.answers else {})
    
    # Obtener preguntas con respuestas
    questions = Question.objects.filter(test_id=result.test_id).prefetch_related('answers')
    
    question_details = []
    for idx, question in enumerate(questions, 1):
        answers_detail = []
        user_selected_answer = user_answers.get(str(question.pk))
        
        for answer in question.answers.all():
            answers_detail.append({
                'id': answer.pk,
                'answer_text': answer.answer_text,
                'is_correct': answer.is_correct,
                'is_selected': user_selected_answer == answer.pk
            })
        
        is_correct = user_selected_answer and any(
            a.pk == user_selected_answer and a.is_correct 
            for a in question.answers.all()
        )
        
        question_details.append({
            'id': question.pk,
            'question_number': idx,
            'question_text': question.question_text,
            'answers': answers_detail,
            'user_answer_id': user_selected_answer,
            'is_correct_answered': is_correct if user_selected_answer else None
        })
    
    total_questions = len(question_details)
    score_percentage = round((result.correct_answers / total_questions * 100), 1) if total_questions > 0 and result.status == 'completed' else 0
    
    return JsonResponse({
        'result': {
            'id': result.pk,
            'user_id': result.user_id,
            'test_id': result.test_id,
            'correct_answers': result.correct_answers,
            'wrong_answers': result.wrong_answers,
            'time_taken': result.time_taken,
            'time_formatted': format_time(result.time_taken),
            'avg_time_per_question': round(result.time_taken / total_questions, 1) if total_questions > 0 and result.status == 'completed' else 0,
            'status': result.status,
            'answered_questions': user_answers,
            'answered_count': len(user_answers),
            'started_at': result.started_at.isoformat(),
            'updated_at': result.updated_at.isoformat(),
        },
        'user': {
            'id': user.pk,
            'username': user.username,
            'role': user.role,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'registered_at': user.registered_at.isoformat() if user.registered_at else None,
        },
        'test': {
            'id': result.test.id,
            'title': result.test.title,
            'description': result.test.description,
            'main_topic': result.test.main_topic,
            'sub_topic': result.test.sub_topic,
            'specific_topic': result.test.specific_topic,
            'level': result.test.level,
            'created_at': result.test.created_at.isoformat(),
            'total_questions': total_questions,
        },
        'questions': question_details,
        'total_questions': total_questions,
        'score_details': {
            'correct': result.correct_answers,
            'wrong': result.wrong_answers,
            'score_percentage': score_percentage,
        }
    })