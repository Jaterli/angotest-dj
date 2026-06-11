# results/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.paginator import Paginator
from functools import wraps
import json
import logging

from apps.test.models import Test, Question, Answer
from apps.shared.models import get_main_topics, get_predefined_levels, get_predefined_status
from .models import Result

from django.db.models import Q, Sum, Count, F, Case, When, Value, FloatField
from django.db.models.functions import Coalesce, Round
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
import json

User = get_user_model()
logger = logging.getLogger(__name__)

# Decorador para verificar autenticación
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'usuario no autenticado'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

# ====== Guardar o actualizar resultado ======

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def save_or_update_result(request, test_id):
    """Guardar o actualizar resultado (progreso o finalización)"""
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Validar campos requeridos
    if 'status' not in data:
        return JsonResponse({'error': 'status is required'}, status=400)
    
    # Validar status
    status = data.get('status')
    if status not in ['in_progress', 'completed', 'expired']:
        return JsonResponse({'error': 'status debe ser in_progress, completed o expired'}, status=400)
    
    # Verificar que el test existe
    try:
        test = Test.objects.get(id=test_id)
    except Test.DoesNotExist:
        return JsonResponse({'error': 'test no encontrado'}, status=404)
    
    user_id = request.user.id
    answers = data.get('answers', {})
    time_taken = data.get('time_taken', 0)
    
    # Buscar resultado existente
    result = Result.objects.filter(
        user_id=user_id,
        test_id=test_id,
        status='in_progress'
    ).first()
    
    # Preparar respuestas en JSON
    answers_json = json.dumps(answers) if answers else ''
    
    # Calcular puntuación si está completado
    correct_count = 0
    wrong_count = 0
    
    if status == 'completed' and answers:
        # Obtener respuestas correctas del test
        questions = Question.objects.filter(test_id=test_id).prefetch_related('answers')
        correct_answers = {}
        
        for question in questions:
            for answer in question.answers.all():
                if answer.is_correct:
                    correct_answers[question.id] = answer.id
                    break
        
        # Calcular respuestas correctas
        for question_id, user_answer_id in answers.items():
            try:
                q_id = int(question_id)
                u_answer_id = int(user_answer_id)
                if correct_answers.get(q_id) == u_answer_id:
                    correct_count += 1
                else:
                    wrong_count += 1
            except (ValueError, TypeError):
                wrong_count += 1
    
    if not result:
        # Crear nuevo resultado
        result = Result.objects.create(
            user_id=user_id,
            test_id=test_id,
            status=status,
            time_taken=time_taken,
            correct_answers=correct_count,
            wrong_answers=wrong_count,
            answers=answers_json
        )
    else:
        # Actualizar resultado existente
        result.status = status
        result.time_taken = time_taken
        result.updated_at = timezone.now()
        
        if status == 'completed':
            result.correct_answers = correct_count
            result.wrong_answers = wrong_count
        
        if answers:
            result.answers = answers_json
        
        result.save()
    
    # Calcular porcentaje
    total_answers = len(answers)
    score_percentage = 0
    if total_answers > 0:
        score_percentage = (correct_count / total_answers) * 100
    
    response = {
        'message': 'Resultado guardado exitosamente',
        'result_id': result.id,
        'test_id': result.test_id,
        'status': result.status,
        'correct_answers': result.correct_answers,
        'wrong_answers': result.wrong_answers,
        'total': total_answers,
        'time_taken': result.time_taken,
        'score_percentage': round(score_percentage, 2)
    }
    
    return JsonResponse(response)

# ====== Obtener progreso actual de un test ======

@require_http_methods(["GET"])
@login_required
def get_test_progress(request, test_id):
    """Obtener progreso actual de un test"""
    
    user_id = request.user.id
    
    # Buscar resultado en progreso
    result = Result.objects.filter(
        user_id=user_id,
        test_id=test_id,
        status='in_progress'
    ).first()
    
    if not result:
        # No hay progreso guardado, devolver test sin respuestas
        try:
            test = Test.objects.prefetch_related('questions__answers').get(id=test_id)
        except Test.DoesNotExist:
            return JsonResponse({'error': 'test no encontrado'}, status=404)
        
        return JsonResponse({
            'test': test_to_dict(test),
            'answers': {},
            'time_elapsed': 0,
            'progress': 0,
            'is_resuming': False
        })
    
    # Obtener test completo
    try:
        test = Test.objects.prefetch_related('questions__answers').get(id=test_id)
    except Test.DoesNotExist:
        return JsonResponse({'error': 'test no encontrado'}, status=404)
    
    # Decodificar respuestas guardadas
    saved_answers = {}
    if result.answers:
        try:
            saved_answers = json.loads(result.answers)
        except json.JSONDecodeError:
            saved_answers = {}
    
    # Calcular progreso
    total_questions = test.questions.count()
    progress = 0
    if total_questions > 0:
        progress = (len(saved_answers) / total_questions) * 100
    
    return JsonResponse({
        'test': test_to_dict(test),
        'answers': saved_answers,
        'time_elapsed': result.time_taken,
        'progress': round(progress, 2),
        'is_resuming': True,
        'result_id': result.id
    })

# ====== Obtener tests en progreso ======

@require_http_methods(["GET"])
@login_required
def get_my_in_progress_tests(request):
    """Obtener tests en progreso del usuario actual con filtros y paginación"""
    
    user_id = request.user.id
    
    # Obtener parámetros de consulta
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    main_topic = request.GET.get('main_topic', '')
    level = request.GET.get('level', '')
    sort_by = request.GET.get('sort_by', 'result_updated_at')
    sort_order = request.GET.get('sort_order', 'desc')
    
    # Validaciones
    if page < 1:
        page = 1
    if page_size < 1 or page_size > 50:
        page_size = 10
    
    # Construir consulta base
    query = Result.objects.filter(
        user_id=user_id,
        status='in_progress'
    ).select_related('test')
    
    # Aplicar filtros
    if main_topic:
        query = query.filter(test__main_topic=main_topic)
    if level:
        query = query.filter(test__level=level)
    
    # Contar total sin filtros (para referencia)
    total_tests = Result.objects.filter(user_id=user_id, status='in_progress').count()
    
    # Contar total filtrado
    total_filtered_tests = query.count()
    
    # Aplicar ordenación
    if sort_by == 'result_updated_at':
        order_field = 'updated_at'
    elif sort_by == 'result_started_at':
        order_field = 'started_at'
    elif sort_by == 'result_time_taken':
        order_field = 'time_taken'
    elif sort_by == 'test_title':
        order_field = 'test__title'
    elif sort_by == 'test_created_at':
        order_field = 'test__created_at'
    elif sort_by == 'test_level':
        order_field = 'test__level'
    else:
        order_field = 'updated_at'
    
    if sort_order == 'desc':
        order_field = f'-{order_field}'
    query = query.order_by(order_field)
    
    # Paginar
    paginator = Paginator(query, page_size)
    page_obj = paginator.get_page(page)
    
    # Construir respuesta
    results_data = []
    total_progress = 0
    total_answered = 0
    total_time = 0
    
    for result in page_obj:
        # Contar respuestas contestadas
        answers = {}
        if result.answers:
            try:
                answers = json.loads(result.answers)
            except json.JSONDecodeError:
                pass
        
        answered_count = len(answers)
        total_questions = result.test.questions.count()
        progress = 0
        if total_questions > 0:
            progress = (answered_count / total_questions) * 100
        
        total_progress += progress
        total_answered += answered_count
        total_time += result.time_taken
        
        # Formatear tiempo empleado
        time_spent = ''
        if result.time_taken > 0:
            hours = result.time_taken // 3600
            minutes = (result.time_taken % 3600) // 60
            seconds = result.time_taken % 60
            
            if hours > 0:
                time_spent = f"{hours}h {minutes}m {seconds}s"
            elif minutes > 0:
                time_spent = f"{minutes}m {seconds}s"
            else:
                time_spent = f"{seconds}s"
        
        results_data.append({
            'result_id': result.id,
            'user_id': result.user_id,
            'test_id': result.test.id,
            'time_taken': result.time_taken,
            'status': result.status,
            'answers': result.answers,
            'started_at': result.started_at.isoformat(),
            'updated_at': result.updated_at.isoformat(),
            'test_title': result.test.title,
            'test_description': result.test.description,
            'test_main_topic': result.test.main_topic,
            'test_sub_topic': result.test.sub_topic,
            'test_specific_topic': result.test.specific_topic,
            'test_level': result.test.level,
            'test_created_at': result.test.created_at.isoformat(),
            'total_questions': total_questions,
            'attempt': 1,  # Por simplificar
            'progress': round(progress, 2),
            'answered_count': answered_count,
            'remaining_count': total_questions - answered_count,
            'time_spent': time_spent
        })
    
    # Ordenar por progreso si se solicitó
    if sort_by == 'progress':
        results_data.sort(key=lambda x: x['progress'], reverse=(sort_order == 'desc'))
    
    if sort_by == 'remaining_count':
        results_data.sort(key=lambda x: x['remaining_count'], reverse=(sort_order == 'desc'))
    
    # Calcular estadísticas
    avg_progress = 0
    if len(results_data) > 0:
        avg_progress = total_progress / len(results_data)
    
    avg_time_per_test = 0
    if total_filtered_tests > 0:
        avg_time_per_test = total_time // total_filtered_tests
    
    # Obtener temas principales
    main_topics = Result.objects.filter(
        user_id=user_id,
        status='in_progress'
    ).exclude(test__main_topic='').values_list('test__main_topic', flat=True).distinct().order_by('test__main_topic')
    
    response = {
        'data': {
            'results': results_data,
            'total_tests': total_tests,
            'total_pages': paginator.num_pages,
            'current_page': page,
            'page_size': page_size,
            'has_more': page < paginator.num_pages,
            'main_topics': list(main_topics)
        },
        'stats': {
            'total_filtered_tests': total_filtered_tests,
            'average_progress': round(avg_progress, 2),
            'total_questions_answered': total_answered,
            'total_time_spent': total_time,
            'avg_time_per_test': avg_time_per_test
        }
    }
    
    return JsonResponse(response)

# ====== Obtener tests completados ======

@require_http_methods(["GET"])
@login_required
def get_my_completed_tests(request):
    """Obtener tests completados del usuario actual con filtros y paginación"""
    
    user_id = request.user.id
    
    # Obtener parámetros de consulta
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    main_topic = request.GET.get('main_topic', '')
    level = request.GET.get('level', '')
    sort_by = request.GET.get('sort_by', 'result_updated_at')
    sort_order = request.GET.get('sort_order', 'desc')
    
    # Validaciones
    if page < 1:
        page = 1
    if page_size < 1 or page_size > 50:
        page_size = 10
    
    # Construir consulta base
    query = Result.objects.filter(
        user_id=user_id,
        status='completed',
        test__is_active=True
    ).select_related('test')
    
    # Aplicar filtros
    if main_topic:
        query = query.filter(test__main_topic=main_topic)
    if level:
        query = query.filter(test__level=level)
    
    # Contar total sin filtros
    total_tests = Result.objects.filter(user_id=user_id, status='completed').count()
    
    # Contar total filtrado
    total_filtered_tests = query.count()
    
    # Aplicar ordenación
    if sort_by == 'result_updated_at':
        order_field = 'updated_at'
    elif sort_by == 'result_started_at':
        order_field = 'started_at'
    elif sort_by == 'result_time_taken':
        order_field = 'time_taken'
    elif sort_by == 'test_title':
        order_field = 'test__title'
    elif sort_by == 'test_created_at':
        order_field = 'test__created_at'
    elif sort_by == 'test_level':
        order_field = 'test__level'
    else:
        order_field = 'updated_at'
    
    if sort_by != 'score' and order_field:
        if sort_order == 'desc':
            order_field = f'-{order_field}'
        query = query.order_by(order_field)
    else:
        query = query.order_by('-updated_at')
    
    # Paginar
    paginator = Paginator(query, page_size)
    page_obj = paginator.get_page(page)
    
    # Construir respuesta
    results_data = []
    total_questions_sum = 0
    total_correct_sum = 0
    total_time_sum = 0
    
    for result in page_obj:
        total_questions = result.test.questions.count()
        score_percent = 0
        accuracy = 0
        
        if total_questions > 0:
            score_percent = (result.correct_answers / total_questions) * 100
        
        total_answered = result.correct_answers + result.wrong_answers
        if total_answered > 0:
            accuracy = (result.correct_answers / total_answered) * 100
        
        total_questions_sum += total_questions
        total_correct_sum += result.correct_answers
        total_time_sum += result.time_taken
        
        results_data.append({
            'result_id': result.id,
            'user_id': result.user_id,
            'test_id': result.test.id,
            'correct_answers': result.correct_answers,
            'wrong_answers': result.wrong_answers,
            'time_taken': result.time_taken,
            'status': result.status,
            'started_at': result.started_at.isoformat(),
            'updated_at': result.updated_at.isoformat(),
            'test_title': result.test.title,
            'test_description': result.test.description,
            'test_main_topic': result.test.main_topic,
            'test_sub_topic': result.test.sub_topic,
            'test_specific_topic': result.test.specific_topic,
            'test_level': result.test.level,
            'test_created_at': result.test.created_at.isoformat(),
            'total_questions': total_questions,
            'attempt': 1,
            'score_percent': round(score_percent, 2),
            'score_rounded': int(round(score_percent)),
            'accuracy': round(accuracy, 2)
        })
    
    # Ordenar por score si se solicitó
    if sort_by == 'score':
        results_data.sort(key=lambda x: x['score_percent'], reverse=(sort_order == 'desc'))
    
    # Calcular estadísticas generales (con filtros)
    avg_score = 0
    if total_questions_sum > 0:
        avg_score = (total_correct_sum / total_questions_sum) * 100
    
    # Obtener temas principales
    main_topics = Result.objects.filter(
        user_id=user_id,
        status='completed'
    ).exclude(test__main_topic='').values_list('test__main_topic', flat=True).distinct().order_by('test__main_topic')
    
    response = {
        'data': {
            'test_results': results_data,
            'total_tests': total_tests,
            'total_pages': paginator.num_pages,
            'current_page': page,
            'page_size': page_size,
            'has_more': page < paginator.num_pages,
            'main_topics': list(main_topics)
        },
        'stats': {
            'average_score': round(avg_score, 2),
            'total_time_spent': total_time_sum,
            'total_filtered_tests': total_filtered_tests,
            'total_questions_answered': total_correct_sum
        }
    }
    
    return JsonResponse(response)

# ====== Eliminar progreso de un test ======

@csrf_exempt
@require_http_methods(["DELETE"])
@login_required
def delete_test_progress(request, test_id):
    """Eliminar progreso de un test"""
    
    user_id = request.user.id
    
    deleted_count, _ = Result.objects.filter(
        user_id=user_id,
        test_id=test_id,
        status='in_progress'
    ).delete()
    
    if deleted_count > 0:
        return JsonResponse({'message': 'progreso eliminado'})
    else:
        return JsonResponse({'message': 'no se encontró progreso para eliminar'})

# ====== Obtener respuestas incorrectas ======

@require_http_methods(["GET"])
@login_required
def get_incorrect_answers(request, result_id):
    """Obtener respuestas incorrectas de un resultado completado"""
    
    user_id = request.user.id
    
    try:
        result = Result.objects.get(id=result_id, user_id=user_id)
    except Result.DoesNotExist:
        return JsonResponse({'error': 'resultado no encontrado'}, status=404)
    
    # Parsear respuestas del usuario - CORREGIDO
    user_answers = {}
    if result.answers:
        if isinstance(result.answers, dict):
            user_answers = result.answers
        elif isinstance(result.answers, str):
            try:
                user_answers = json.loads(result.answers)
            except json.JSONDecodeError:
                user_answers = {}
        else:
            try:
                user_answers = dict(result.answers) if result.answers else {}
            except (TypeError, ValueError):
                user_answers = {}
    
    # Obtener preguntas del test con respuestas correctas
    questions = Question.objects.filter(test_id=result.test_id).prefetch_related('answers')
    
    # Crear mapa de respuestas correctas
    correct_answers = {}
    for question in questions:
        for answer in question.answers.all():
            if answer.is_correct:
                correct_answers[question.id] = {
                    'id': answer.id,
                    'text': answer.answer_text
                }
                break
    
    # Encontrar respuestas incorrectas
    incorrect_questions = []
    question_number = 1
    
    for question in questions:
        user_answer_id = user_answers.get(str(question.id))
        correct_answer = correct_answers.get(question.id)
        
        # Si la respuesta es incorrecta o no existe
        if user_answer_id != correct_answer['id']:
            # Obtener texto de la respuesta del usuario
            user_answer_text = 'No respondida'
            if user_answer_id:
                try:
                    user_answer = Answer.objects.get(id=user_answer_id)
                    user_answer_text = user_answer.answer_text
                except Answer.DoesNotExist:
                    user_answer_text = 'Respuesta no válida'
            
            incorrect_questions.append({
                'question_id': question.id,
                'question_number': question_number,
                'question_text': question.question_text,
                'correct_answer_id': correct_answer['id'],
                'correct_answer_text': correct_answer['text'],
                'user_answer_text': user_answer_text
            })
        
        question_number += 1
    
    # Calcular resumen
    total_questions = result.correct_answers + result.wrong_answers
    score_percentage = 0
    if total_questions > 0:
        score_percentage = (result.correct_answers / total_questions) * 100
    
    response = {
        'incorrect_questions': incorrect_questions,
        'summary': {
            'total_questions': total_questions,
            'total_correct': result.correct_answers,
            'total_incorrect': result.wrong_answers,
            'questions_with_errors': len(incorrect_questions),
            'score_percentage': round(score_percentage, 2)
        }
    }
    
    return JsonResponse(response)



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



# Decorador para verificar admin
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verificar si el usuario está autenticado primero
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'No autenticado'}, status=401)
        
        # Ahora podemos acceder a user.role con seguridad
        if request.user.role != 'admin':
            console_message = f"Acceso denegado para usuario {request.user.id} con rol {request.user.role}"
            return JsonResponse({'error': 'Acceso denegado. Se requieren privilegios de administrador'}, status=403)
        else:
            logger.info(f"Acceso concedido para usuario {request.user.id} con rol {request.user.role}")
        return view_func(request, *args, **kwargs)
    return wrapper


# ====== Admin: Obtener lista de resultados con filtros avanzados ======
@require_http_methods(["GET"])
@admin_required
def get_results_list(request):
    """Obtener lista de resultados con paginación, filtrado y ordenación"""
    
    # Obtener parámetros de consulta
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    sort_by = request.GET.get('sort_by', 'updated_at')
    sort_order = request.GET.get('sort_order', 'desc')
    
    # Filtros de usuario
    user_id = request.GET.get('user_id')
    user_role = request.GET.get('user_role')
    user_email = request.GET.get('user_email')
    user_username = request.GET.get('user_username')
    
    # Filtros de test
    test_id = request.GET.get('test_id')
    test_title = request.GET.get('test_title')
    test_main_topic = request.GET.get('test_main_topic')
    test_sub_topic = request.GET.get('test_sub_topic')
    test_specific_topic = request.GET.get('test_specific_topic')
    test_level = request.GET.get('test_level')
    test_created_by = request.GET.get('test_created_by')
    
    # Filtros de resultado
    status = request.GET.get('status')
    min_score = request.GET.get('min_score')
    max_score = request.GET.get('max_score')
    
    # Filtros de fecha
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Búsqueda general
    search = request.GET.get('search')
    
    # Validaciones
    if page < 1:
        page = 1
    if page_size < 1 or page_size > 100:
        page_size = 20
    
    valid_sort_fields = ['id', 'started_at', 'updated_at', 'time_taken', 
                         'correct_answers', 'user_username', 'test_title', 
                         'test_main_topic', 'test_level', 'score']
    if sort_by not in valid_sort_fields:
        sort_by = 'updated_at'
    
    if sort_order not in ['asc', 'desc']:
        sort_order = 'desc'
    
    # Contar total de resultados
    total_results = Result.objects.count()
    
    # Construir query base con anotaciones
    results_query = Result.objects.select_related('user', 'test').annotate(
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
        ),
        total_questions=F('correct_answers') + F('wrong_answers'),
        user_username=F('user__username'),
        user_email=F('user__email'),
        user_first_name=F('user__first_name'),
        user_last_name=F('user__last_name'),
        user_role=F('user__role'),
        test_title=F('test__title'),
        test_description=F('test__description'),
        test_main_topic=F('test__main_topic'),
        test_sub_topic=F('test__sub_topic'),
        test_specific_topic=F('test__specific_topic'),
        test_level=F('test__level'),
    )
    
    # Aplicar filtros de usuario
    if user_id:
        try:
            results_query = results_query.filter(user_id=int(user_id))
        except ValueError:
            pass
    
    if user_role:
        results_query = results_query.filter(user__role=user_role)
    
    if user_email:
        results_query = results_query.filter(user__email__icontains=user_email)
    
    if user_username:
        results_query = results_query.filter(user__username__icontains=user_username)
    
    # Aplicar filtros de test
    if test_id:
        try:
            results_query = results_query.filter(test_id=int(test_id))
        except ValueError:
            pass
    
    if test_title:
        results_query = results_query.filter(test__title__icontains=test_title)
    
    if test_main_topic:
        results_query = results_query.filter(test__main_topic=test_main_topic)
    
    if test_sub_topic:
        results_query = results_query.filter(test__sub_topic=test_sub_topic)
    
    if test_specific_topic:
        results_query = results_query.filter(test__specific_topic=test_specific_topic)
    
    if test_level:
        results_query = results_query.filter(test__level=test_level)
    
    if test_created_by:
        try:
            results_query = results_query.filter(test__created_by=int(test_created_by))
        except ValueError:
            pass
    
    # Aplicar filtros de resultado
    if status:
        results_query = results_query.filter(status=status)
    
    # Aplicar filtros de puntuación
    if min_score:
        try:
            min_val = float(min_score)
            results_query = results_query.filter(score__gte=min_val)
        except ValueError:
            pass
    
    if max_score:
        try:
            max_val = float(max_score)
            results_query = results_query.filter(score__lte=max_val)
        except ValueError:
            pass
    
    # Aplicar filtros de fecha
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            results_query = results_query.filter(started_at__date__gte=start)
        except ValueError:
            pass
    
    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            results_query = results_query.filter(started_at__date__lte=end)
        except ValueError:
            pass
    
    # Aplicar búsqueda general
    if search:
        results_query = results_query.filter(
            Q(user__username__icontains=search) |
            Q(user__email__icontains=search) |
            Q(test__title__icontains=search) |
            Q(test__main_topic__icontains=search) |
            Q(test__sub_topic__icontains=search)
        )
    
    # Contar total filtrado
    total_filtered_results = results_query.count()
    
    # Aplicar ordenación
    if sort_order == 'desc':
        sort_by = f'-{sort_by}'
    results_query = results_query.order_by(sort_by)
    
    # Aplicar paginación
    offset = (page - 1) * page_size
    results_list = list(results_query[offset:offset + page_size])
    
    # Convertir a diccionarios para la respuesta
    results_data = []
    for result in results_list:
        results_data.append({
            'id': result.id,
            'user_id': result.user_id,
            'test_id': result.test_id,
            'correct_answers': result.correct_answers,
            'wrong_answers': result.wrong_answers,
            'total_questions': result.total_questions,
            'score': float(result.score) if result.score else 0,
            'time_taken': result.time_taken,
            'status': result.status,
            'answers': result.answers,
            'started_at': result.started_at.isoformat() if result.started_at else None,
            'updated_at': result.updated_at.isoformat() if result.updated_at else None,
            'user_username': result.user_username,
            'user_email': result.user_email,
            'user_first_name': result.user_first_name,
            'user_last_name': result.user_last_name,
            'user_role': result.user_role,
            'test_title': result.test_title,
            'test_description': result.test_description,
            'test_main_topic': result.test_main_topic,
            'test_sub_topic': result.test_sub_topic,
            'test_specific_topic': result.test_specific_topic,
            'test_level': result.test_level,
        })
    
    # Obtener filtros disponibles
    main_topics = get_main_topics()
    levels = get_predefined_levels()
    statuses = get_predefined_status()
    
    return JsonResponse({
        'results': results_data,
        'filters_applied': {
            'page': page,
            'page_size': page_size,
            'sort_by': sort_by.lstrip('-') if sort_by.startswith('-') else sort_by,
            'sort_order': sort_order,
            'user_id': user_id,
            'user_role': user_role,
            'user_email': user_email,
            'user_username': user_username,
            'test_id': test_id,
            'test_title': test_title,
            'test_main_topic': test_main_topic,
            'test_sub_topic': test_sub_topic,
            'test_specific_topic': test_specific_topic,
            'test_level': test_level,
            'test_created_by': test_created_by,
            'status': status,
            'min_score': min_score,
            'max_score': max_score,
            'start_date': start_date,
            'end_date': end_date,
            'search': search,
        },
        'available_filters': {
            'main_topics': main_topics,
            'levels': levels,
            'statuses': statuses,
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
    try:
        result = Result.objects.get(id=result_id)
    except Result.DoesNotExist:
        return JsonResponse({'error': 'Resultado no encontrado'}, status=404)
    
    result.delete()
    
    return JsonResponse({
        'message': 'Resultado eliminado',
        'id': result_id
    })


# ====== Eliminar múltiples resultados (Bulk Delete) ======
@csrf_exempt
@require_http_methods(["POST"])
@admin_required
def delete_results_bulk(request):
    """Eliminar múltiples resultados"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    ids = data.get('ids', [])
    if not ids or not isinstance(ids, list) or len(ids) < 1:
        return JsonResponse({'error': 'Se requiere una lista de IDs con al menos un elemento'}, status=400)
    
    # Validar que todos los IDs sean enteros
    try:
        ids = [int(id_val) for id_val in ids]
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Los IDs deben ser números enteros'}, status=400)
    
    # Eliminar resultados
    deleted_count, _ = Result.objects.filter(id__in=ids).delete()
    
    return JsonResponse({
        'message': f'{deleted_count} resultados eliminados',
        'deleted_count': deleted_count
    })


# ====== Resultados de Usuario (Admin) ======

@require_http_methods(["GET"])
@admin_required
def get_user_results(request, user_id):
    """Obtener resultados de tests de un usuario específico"""
    
    # Verificar que el usuario existe
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'usuario no encontrado'}, status=404)
    
    # Obtener parámetros de consulta
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    status = request.GET.get('status', 'all')
    sort_by = request.GET.get('sort_by', 'updated_at')
    sort_order = request.GET.get('sort_order', 'desc')
    search = request.GET.get('search', '')
    level = request.GET.get('level', '')
    main_topic = request.GET.get('main_topic', '')
    sub_topic = request.GET.get('sub_topic', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    
    # Validaciones
    if page < 1:
        page = 1
    if page_size < 1 or page_size > 100:
        page_size = 20
    
    valid_sort_fields = ['started_at', 'updated_at', 'test_created_at', 'title', 'level', 'average_score', 'time_taken']
    if sort_by not in valid_sort_fields:
        sort_by = 'updated_at'
    
    if sort_order not in ['asc', 'desc']:
        sort_order = 'desc'
    
    # Construir consulta base
    query = Result.objects.filter(
        user_id=user_id
    ).select_related('test')
    
    # Contar total de resultados (sin filtros)
    total_results = query.count()
    
    # Aplicar filtros
    if status and status != 'all':
        query = query.filter(status=status)
    
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
    
    # Contar total filtrado
    total_filtered_results = query.count()
    
    # Calcular estadísticas (usando los mismos filtros)
    stats = query.aggregate(
        completed_tests=Count('id', filter=Q(status='completed')),
        in_progress_tests=Count('id', filter=Q(status='in_progress')),
        total_time_spent=Coalesce(Sum('time_taken'), Value(0)),
        total_questions_answered=Coalesce(
            Sum(Case(When(status='completed', then=F('correct_answers') + F('wrong_answers')), default=Value(0))),
            Value(0)
        ),
        total_correct_answers=Coalesce(
            Sum(Case(When(status='completed', then='correct_answers'), default=Value(0))),
            Value(0)
        )
    )
    
    # Calcular promedio de score
    avg_score = 0.0
    if stats['total_questions_answered'] and stats['total_questions_answered'] > 0:
        avg_score = (stats['total_correct_answers'] / stats['total_questions_answered']) * 100
        avg_score = round(avg_score, 1)
    
    # Aplicar ordenación
    if sort_by == 'title':
        order_field = 'test__title'
    elif sort_by == 'level':
        order_field = 'test__level'
    elif sort_by == 'test_created_at':
        order_field = 'test__created_at'
    elif sort_by == 'average_score':
        # Ordenar después de calcular
        order_field = None
    else:
        order_field = sort_by
    
    if order_field:
        if sort_order == 'desc':
            order_field = f'-{order_field}'
        query = query.order_by(order_field)
    else:
        query = query.order_by('-updated_at')
    
    # Paginar
    paginator = Paginator(query, page_size)
    page_obj = paginator.get_page(page)
    
    # Convertir resultados
    results_data = []
    for result in page_obj:
        total_questions = result.test.questions.count()
        score = 0
        if total_questions > 0 and result.status == 'completed':
            score = (result.correct_answers / total_questions) * 100
            score = round(score, 1)
        
        # Calcular answered_count
        answered_count = 0
        if result.status == 'completed':
            answered_count = result.correct_answers + result.wrong_answers
        elif result.status == 'in_progress' and result.answers:
            try:
                answers = json.loads(result.answers)
                answered_count = len(answers)
            except json.JSONDecodeError:
                pass
        
        results_data.append({
            'id': result.id,
            'test_id': result.test.id,
            'correct_answers': result.correct_answers,
            'wrong_answers': result.wrong_answers,
            'total_questions': total_questions,
            'score': score,
            'time_taken': result.time_taken,
            'status': result.status,
            'started_at': result.started_at.isoformat(),
            'updated_at': result.updated_at.isoformat(),
            'test_title': result.test.title,
            'test_description': result.test.description,
            'test_main_topic': result.test.main_topic,
            'test_sub_topic': result.test.sub_topic,
            'test_specific_topic': result.test.specific_topic,
            'test_level': result.test.level,
            'test_created_at': result.test.created_at.isoformat(),
            'answered_count': answered_count
        })
    
    # Ordenar por average_score si se solicitó (después de calcular)
    if sort_by == 'average_score':
        results_data.sort(key=lambda x: x['score'], reverse=(sort_order == 'desc'))
        
    main_topics = get_main_topics()
    levels = get_predefined_levels()
    
    # Construir respuesta
    response = {
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'registered_at': user.registered_at.isoformat() if user.registered_at else None,
        },
        'results': results_data,
        'filters_applied': {
            'page': page,
            'page_size': page_size,
            'sort_by': sort_by,
            'sort_order': sort_order,
            'status': status,
            'level': level,
            'main_topic': main_topic,
            'sub_topic': sub_topic,
            'from_date': from_date,
            'to_date': to_date,
            'search': search,
        },
        'available_filters': {
            'main_topics': main_topics,
            'levels': levels,
            'statuses': ['all', 'completed', 'in_progress'],
        },
        'stats': {
            'total_results': total_results,
            'total_filtered_results': total_filtered_results,
            'completed_tests': stats['completed_tests'] or 0,
            'in_progress_tests': stats['in_progress_tests'] or 0,
            'average_score': avg_score,
            'total_time_spent': stats['total_time_spent'] or 0,
            'total_questions_answered': stats['total_questions_answered'] or 0,
            'total_correct_answers': stats['total_correct_answers'] or 0,
        }
    }
    
    return JsonResponse(response)


@require_http_methods(["GET"])
@admin_required
def get_user_result_details(request, result_id, user_id=None):
    """Obtener detalles específicos de un resultado"""
    
    # Si se proporciona user_id, verificar que coincida
    if user_id and request.user.id != int(user_id) and request.user.role != 'admin':
        return JsonResponse({'error': 'no autorizado'}, status=403)
    
    # Usar el user_id de la URL o el del usuario autenticado
    target_user_id = user_id if user_id else request.user.id
    
    # Verificar que el usuario existe
    try:
        user = User.objects.get(id=target_user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'usuario no encontrado'}, status=404)
    
    # Obtener resultado con relaciones
    try:
        result = Result.objects.select_related('test').get(
            id=result_id,
            user_id=target_user_id
        )
    except Result.DoesNotExist:
        return JsonResponse({'error': 'resultado no encontrado'}, status=404)
    
    # Parsear respuestas del usuario - CORREGIDO
    user_answers = {}
    if result.answers:
        # Si ya es un diccionario, usarlo directamente
        if isinstance(result.answers, dict):
            user_answers = result.answers
        # Si es una cadena, parsearla
        elif isinstance(result.answers, str):
            try:
                user_answers = json.loads(result.answers)
            except json.JSONDecodeError:
                user_answers = {}
        # Si es otro tipo, intentar convertirlo
        else:
            try:
                user_answers = dict(result.answers) if result.answers else {}
            except (TypeError, ValueError):
                user_answers = {}
    
    # Obtener todas las preguntas con sus respuestas
    questions = Question.objects.filter(test_id=result.test_id).prefetch_related('answers')
    
    # Procesar preguntas y respuestas
    question_details = []
    for idx, question in enumerate(questions, 1):
        answers_detail = []
        for answer in question.answers.all():
            # Verificar si esta respuesta fue seleccionada por el usuario
            is_selected = str(question.id) in user_answers and user_answers.get(str(question.id)) == answer.id
        
        answers_detail.append({
            'id': answer.id,
            'answer_text': answer.answer_text,
            'is_correct': answer.is_correct,
            'is_selected': is_selected
        })
        
        question_details.append({
            'id': question.id,
            'question_number': idx,
            'question_text': question.question_text,
            'answers': answers_detail,
            'user_answer_id': user_answers.get(str(question.id)),
            'is_correct_answered': (user_answers.get(str(question.id)) == next(
                (a.id for a in question.answers.all() if a.is_correct), None
            )) if str(question.id) in user_answers else None
        })
    
    # Calcular score
    total_questions = len(question_details)
    score_percentage = 0
    if total_questions > 0 and result.status == 'completed':
        score_percentage = (result.correct_answers / total_questions) * 100
        score_percentage = round(score_percentage, 1)
    
    # Formatear tiempo
    time_formatted = ''
    if result.time_taken > 0:
        hours = result.time_taken // 3600
        minutes = (result.time_taken % 3600) // 60
        seconds = result.time_taken % 60
        
        if hours > 0:
            time_formatted = f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            time_formatted = f"{minutes}m {seconds}s"
        else:
            time_formatted = f"{seconds}s"
    
    # Calcular tiempo promedio por pregunta
    avg_time_per_question = 0
    if total_questions > 0 and result.status == 'completed':
        avg_time_per_question = round(result.time_taken / total_questions, 1)
    
    response = {
        'result': {
            'id': result.id,
            'user_id': result.user_id,
            'test_id': result.test_id,
            'correct_answers': result.correct_answers,
            'wrong_answers': result.wrong_answers,
            'time_taken': result.time_taken,
            'time_formatted': time_formatted,
            'avg_time_per_question': avg_time_per_question,
            'status': result.status,
            'answered_questions': user_answers,
            'answered_count': len(user_answers),
            'started_at': result.started_at.isoformat(),
            'updated_at': result.updated_at.isoformat(),
        },
        'user': {
            'id': user.id,
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
    }
    
    return JsonResponse(response)