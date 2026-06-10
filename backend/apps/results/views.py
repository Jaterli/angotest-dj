# results/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.paginator import Paginator
from functools import wraps
import json

from apps.tests.models import Test, Question, Answer
from .models import Result

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
    
    # 1. Obtener el resultado
    try:
        result = Result.objects.get(id=result_id, user_id=user_id)
    except Result.DoesNotExist:
        return JsonResponse({'error': 'resultado no encontrado'}, status=404)
    
    # 2. Parsear respuestas del usuario
    user_answers = {}
    if result.answers:
        try:
            user_answers = json.loads(result.answers)
        except json.JSONDecodeError:
            user_answers = {}
    
    # 3. Obtener preguntas del test con respuestas correctas
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
    
    # 4. Encontrar respuestas incorrectas
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
    
    # 5. Calcular resumen
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