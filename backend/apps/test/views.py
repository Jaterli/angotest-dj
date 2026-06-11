# tests/views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Count
from django.core.paginator import Paginator
from functools import wraps
import json

from apps.test.models import Test, Question, Answer
from apps.results.models import Result
from apps.shared.models import get_main_topics

# Decorador para verificar autenticación
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'usuario no autenticado'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

# ====== Vistas de Tests ======

@require_http_methods(["GET"])
@login_required
def get_test_by_id(request, test_id):
    """Obtener test por ID con preguntas y respuestas"""
    try:
        test = Test.objects.prefetch_related('questions__answers').get(id=test_id)
    except Test.DoesNotExist:
        return JsonResponse({'error': 'test no encontrado'}, status=404)
    
    return JsonResponse({'test': test_to_dict(test)})

@require_http_methods(["GET"])
@login_required
def get_not_started_tests(request):
    """Obtener tests no iniciados por el usuario con filtros y paginación"""
    
    user_id = request.user.id
    
    # Obtener parámetros de consulta
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    main_topic = request.GET.get('main_topic', '')
    level = request.GET.get('level', '')
    sort_by = request.GET.get('sort_by', 'test_created_at')
    sort_order = request.GET.get('sort_order', 'desc')
    
    # Validaciones
    if page < 1:
        page = 1
    if page_size < 1 or page_size > 50:
        page_size = 10
    
    valid_sort_fields = ['test_title', 'test_created_at', 'test_updated_at', 'test_level', 'questions']
    if sort_by not in valid_sort_fields:
        sort_by = 'test_created_at'
    
    # Obtener IDs de tests donde el usuario tiene resultados
    user_result_test_ids = Result.objects.filter(
        user_id=user_id
    ).values_list('test_id', flat=True).distinct()
    
    # Construir consulta base
    query = Test.objects.filter(is_active=True)
    
    # Excluir tests donde el usuario tiene resultados
    if user_result_test_ids:
        query = query.exclude(id__in=user_result_test_ids)
    
    # Contar totales por nivel ANTES de aplicar filtros
    level_counts = query.values('level').annotate(count=Count('id'))
    total_by_level = {item['level']: item['count'] for item in level_counts}
    total_tests = sum(total_by_level.values())
    
    # Aplicar filtros adicionales
    if main_topic and main_topic != 'all':
        query = query.filter(main_topic=main_topic)
    if level and level != 'all':
        query = query.filter(level=level)
    
    # Contar total filtrado
    total_filtered_tests = query.count()
    
    # Aplicar ordenación
    if sort_by == 'test_title':
        order_field = 'title'
    elif sort_by == 'test_level':
        order_field = 'level'
    elif sort_by == 'test_created_at':
        order_field = 'created_at'
    elif sort_by == 'test_updated_at':
        order_field = 'updated_at'
    elif sort_by == 'questions':
        order_field = 'created_at'  # Por defecto
    else:
        order_field = 'created_at'
    
    if sort_order == 'desc':
        order_field = f'-{order_field}'
    query = query.order_by(order_field)
    
    # Paginar
    paginator = Paginator(query, page_size)
    page_obj = paginator.get_page(page)
    
    # Obtener conteos de preguntas
    test_ids = [test.id for test in page_obj]
    question_counts = Question.objects.filter(
        test_id__in=test_ids
    ).values('test_id').annotate(count=Count('id'))
    questions_map = {item['test_id']: item['count'] for item in question_counts}
    
    # Construir respuesta
    tests_data = []
    for test in page_obj:
        tests_data.append({
            'id': test.id,
            'title': test.title,
            'description': test.description,
            'main_topic': test.main_topic,
            'sub_topic': test.sub_topic,
            'specific_topic': test.specific_topic,
            'level': test.level,
            'is_active': test.is_active,
            'created_by': test.created_by.id if test.created_by else None,
            'created_at': test.created_at.isoformat(),
            'updated_at': test.updated_at.isoformat(),
            'total_questions': questions_map.get(test.id, 0)
        })
    
    # Obtener temas principales
    main_topics = get_main_topics()
    
    response = {
        'data': {
            'tests': tests_data,
            'total_tests': total_tests,
            'total_pages': paginator.num_pages,
            'current_page': page,
            'page_size': page_size,
            'has_more': page < paginator.num_pages,
            'main_topics': main_topics,
        },
        'stats': {
            'total_tests': total_tests,
            'total_filtered_tests': total_filtered_tests,
            'total_by_level': total_by_level,
        }
    }
    
    return JsonResponse(response)

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
    required_fields = ['test_id', 'status']
    for field in required_fields:
        if field not in data:
            return JsonResponse({'error': f'{field} is required'}, status=400)
    
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
            'attempt': 1,  # Por simplificar, siempre es el primer intento
            'progress': round(progress, 2),
            'answered_count': answered_count,
            'remaining_count': total_questions - answered_count,
            'time_spent': time_spent
        })
    
    # Calcular promedio de progreso
    avg_progress = 0
    if len(results_data) > 0:
        avg_progress = total_progress / len(results_data)
    
    # Calcular tiempo promedio por test
    total_time = sum(r.time_taken for r in page_obj)
    avg_time_per_test = 0
    if total_filtered_tests > 0:
        avg_time_per_test = total_time // total_filtered_tests
    
    # Obtener temas principales únicos
    main_topics = Result.objects.filter(
        user_id=user_id,
        status='in_progress'
    ).exclude(test__main_topic='').values_list('test__main_topic', flat=True).distinct().order_by('test__main_topic')
    
    response = {
        'data': {
            'results': results_data,
            'total_tests': Result.objects.filter(user_id=user_id, status='in_progress').count(),
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
    elif sort_by == 'score':
        order_field = 'updated_at'  # Se ordenará después
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
    for result in page_obj:
        total_questions = result.test.questions.count()
        score_percent = 0
        accuracy = 0
        
        if total_questions > 0:
            score_percent = (result.correct_answers / total_questions) * 100
        
        total_answered = result.correct_answers + result.wrong_answers
        if total_answered > 0:
            accuracy = (result.correct_answers / total_answered) * 100
        
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
            'attempt': 1,  # Por simplificar
            'score_percent': round(score_percent, 2),
            'score_rounded': int(round(score_percent)),
            'accuracy': round(accuracy, 2)
        })
    
    # Ordenar por score si se solicitó
    if sort_by == 'score':
        results_data.sort(key=lambda x: x['score_percent'], reverse=(sort_order == 'desc'))
    
    # Calcular estadísticas
    stats_query = Result.objects.filter(
        user_id=user_id,
        status='completed'
    ).select_related('test')
    
    if main_topic:
        stats_query = stats_query.filter(test__main_topic=main_topic)
    if level:
        stats_query = stats_query.filter(test__level=level)
    
    total_questions_sum = 0
    total_correct_sum = 0
    total_time_sum = 0
    
    for result in stats_query:
        q_count = result.test.questions.count()
        total_questions_sum += q_count
        total_correct_sum += result.correct_answers
        total_time_sum += result.time_taken
    
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
            'total_tests': Result.objects.filter(user_id=user_id, status='completed').count(),
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

@require_http_methods(["GET"])
@login_required
def get_incorrect_answers(request, result_id):
    """Obtener respuestas incorrectas de un resultado completado"""
    
    user_id = request.user.id
    
    try:
        result = Result.objects.get(id=result_id, user_id=user_id)
    except Result.DoesNotExist:
        return JsonResponse({'error': 'resultado no encontrado'}, status=404)
    
    # Parsear respuestas del usuario
    user_answers = {}
    if result.answers:
        try:
            user_answers = json.loads(result.answers)
        except json.JSONDecodeError:
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

# Funciones auxiliares
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
        'created_by': test.created_by.id if test.created_by else None,
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





# ====== Vistas de Preguntas ======

@require_http_methods(["GET"])
@login_required
def get_test_questions(request, test_id):
    """Obtener todas las preguntas de un test (paginadas)"""
    
    # Validar test_id
    try:
        test_id = int(test_id)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'ID de test inválido'}, status=400)
    
    # Verificar que el test existe
    try:
        test = Test.objects.get(id=test_id)
    except Test.DoesNotExist:
        return JsonResponse({'error': 'test no encontrado'}, status=404)
    
    # Obtener parámetros de paginación
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10
    
    user_id = request.user.id
    
    # Verificar si el usuario tiene progreso en este test
    result = Result.objects.filter(
        user_id=user_id,
        test_id=test_id
    ).exclude(status='completed').first()
    
    has_progress = result is not None
    
    # Obtener total de preguntas
    total_questions = Question.objects.filter(test_id=test_id).count()
    
    # Obtener preguntas paginadas (sin respuestas correctas)
    questions_query = Question.objects.filter(test_id=test_id)
    
    paginator = Paginator(questions_query, page_size)
    page_obj = paginator.get_page(page)
    
    # Obtener respuestas para cada pregunta (sin incluir is_correct)
    question_responses = []
    for question in page_obj:
        answers = Answer.objects.filter(question_id=question.id).values('id', 'answer_text')
        
        question_responses.append({
            'id': question.id,
            'question_text': question.question_text,
            'answers': list(answers)
        })
    
    # Obtener progreso si existe
    progress = 0.0
    if has_progress and result.answers:
        try:
            saved_answers = json.loads(result.answers)
            if total_questions > 0:
                progress = (len(saved_answers) / total_questions) * 100
        except json.JSONDecodeError:
            pass
    
    response = {
        'test_id': test_id,
        'total': total_questions,
        'page': page,
        'page_size': page_size,
        'questions': question_responses,
        'progress': round(progress, 2)
    }
    
    return JsonResponse(response)


@require_http_methods(["GET"])
@login_required
def get_single_question(request, test_id, question_number):
    """Obtener una pregunta específica por número"""
    
    # Validar parámetros
    try:
        test_id = int(test_id)
        question_number = int(question_number)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'ID de test o número de pregunta inválido'}, status=400)
    
    if question_number < 1:
        return JsonResponse({'error': 'número de pregunta inválido'}, status=400)
    
    # Verificar que el test existe
    try:
        test = Test.objects.get(id=test_id)
    except Test.DoesNotExist:
        return JsonResponse({'error': 'test no encontrado'}, status=404)
    
    # Obtener la pregunta específica (offset = question_number - 1)
    try:
        question = Question.objects.filter(test_id=test_id).order_by('id')[question_number - 1]
    except IndexError:
        return JsonResponse({'error': 'pregunta no encontrada'}, status=404)
    
    # Obtener respuestas (sin is_correct)
    answers = Answer.objects.filter(question_id=question.id).values('id', 'answer_text')
    
    # Obtener total de preguntas para el progreso
    total_questions = Question.objects.filter(test_id=test_id).count()
    
    response = {
        'question': {
            'id': question.id,
            'question_text': question.question_text,
            'answers': list(answers)
        },
        'question_number': question_number,
        'total_questions': total_questions,
        'has_next': question_number < total_questions,
        'has_previous': question_number > 1
    }
    
    return JsonResponse(response)


@require_http_methods(["GET"])
@login_required
def get_next_unanswered_question(request, test_id):
    """Obtener la siguiente pregunta sin responder"""
    
    # Validar test_id
    try:
        test_id = int(test_id)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'ID de test inválido'}, status=400)
    
    # Verificar que el test existe
    try:
        test = Test.objects.get(id=test_id)
    except Test.DoesNotExist:
        return JsonResponse({'error': 'test no encontrado'}, status=404)
    
    user_id = request.user.id
    
    # Verificar resultado existente (no completado)
    result = Result.objects.filter(
        user_id=user_id,
        test_id=test_id
    ).exclude(status='completed').first()
    
    # Decodificar respuestas respondidas
    answered_question_ids = set()
    if result and result.answers:
        try:
            saved_answers = json.loads(result.answers)
            answered_question_ids = set(int(qid) for qid in saved_answers.keys())
        except json.JSONDecodeError:
            pass
    
    # Obtener total de preguntas
    total_questions = Question.objects.filter(test_id=test_id).count()
    
    # Si ya respondió todas las preguntas
    if len(answered_question_ids) >= total_questions:
        return JsonResponse({
            'message': 'todas_las_preguntas_respondidas',
            'is_completed': True,
            'answered_count': len(answered_question_ids),
            'total_questions': total_questions,
            'progress': 100.0
        })
    
    # Obtener la primera pregunta sin responder
    questions_query = Question.objects.filter(test_id=test_id)
    
    if answered_question_ids:
        questions_query = questions_query.exclude(id__in=list(answered_question_ids))
    
    question = questions_query.order_by('id').first()
    
    if not question:
        return JsonResponse({
            'error': 'no se encontró pregunta sin responder'
        }, status=404)
    
    # Obtener respuestas (sin is_correct)
    answers = Answer.objects.filter(question_id=question.id).values('id', 'answer_text')
    
    # Calcular número de pregunta (posición)
    question_number = Question.objects.filter(
        test_id=test_id,
        id__lte=question.id
    ).count()
    
    progress = (len(answered_question_ids) / total_questions) * 100 if total_questions > 0 else 0
    
    response = {
        'question': {
            'id': question.id,
            'question_text': question.question_text,
            'answers': list(answers)
        },
        'question_number': question_number,
        'total_questions': total_questions,
        'is_completed': False,
        'answered_count': len(answered_question_ids),
        'progress': round(progress, 2)
    }
    
    return JsonResponse(response)