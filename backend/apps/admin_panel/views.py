# admin/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.db.models import Count, Avg, Q, F, FloatField, Case, When, Value, Sum
from django.utils import timezone
from functools import wraps
import json
import logging

from .models import UserQuota, SystemConfig
from apps.test.models import Test, Question, Answer
from apps.results.models import Result
from apps.invitations.models import TestInvitation
from apps.shared.models import insert_or_update_topic, delete_orphaned_topics, invalidate_topics_cache, get_main_topics, get_sub_topics, get_predefined_levels, get_predefined_status
from apps.accounts.models import PasswordResetToken

from django.db.models.functions import Coalesce, Cast, Round
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.http import HttpResponse

User = get_user_model()
logger = logging.getLogger(__name__)


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


@csrf_exempt
@require_http_methods(["POST"])
@admin_required
def create_test(request):
    """Crear un nuevo test (solo admin)"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Validaciones de campos requeridos
    required_fields = ['title', 'main_topic', 'sub_topic', 'specific_topic', 'level', 'questions']
    for field in required_fields:
        if field not in data:
            return JsonResponse({'error': f'{field} is required'}, status=400)
    
    # Validar nivel
    valid_levels = get_predefined_levels()
    level = data.get('level')
    if level not in valid_levels:
        return JsonResponse({
            'error': 'Nivel no válido',
            'valid_levels': valid_levels
        }, status=400)
    
    # Insertar o actualizar temas
    main_topic = data.get('main_topic')
    sub_topic = data.get('sub_topic')
    specific_topic = data.get('specific_topic')
    
    if not main_topic or not sub_topic or not specific_topic:
        return JsonResponse({'error': 'Faltan temas'}, status=400)
    
    try:
        insert_or_update_topic(main_topic, sub_topic, specific_topic, is_predefined=False)
        invalidate_topics_cache()
    except Exception as e:
        logger.warning(f"No se pudo guardar nuevo tema: {str(e)}")
    
    # Validar preguntas
    questions_data = data.get('questions', [])
    if len(questions_data) == 0:
        return JsonResponse({'error': 'El test debe contener al menos una pregunta'}, status=400)
    
    for i, question in enumerate(questions_data):
        question_text = question.get('question_text', '').strip()
        if not question_text:
            return JsonResponse({
                'error': f'La pregunta {i+1} no tiene texto'
            }, status=400)
        
        answers = question.get('answers', [])
        if len(answers) < 2:
            return JsonResponse({
                'error': f'La pregunta {i+1} debe tener al menos 2 respuestas'
            }, status=400)
        
        correct_count = 0
        for j, answer in enumerate(answers):
            answer_text = answer.get('answer_text', '').strip()
            if not answer_text:
                return JsonResponse({
                    'error': f'La respuesta {j+1} de la pregunta {i+1} no tiene texto'
                }, status=400)
            if answer.get('is_correct', False):
                correct_count += 1
        
        if correct_count != 1:
            return JsonResponse({
                'error': f'La pregunta {i+1} debe tener exactamente una respuesta correcta (tiene {correct_count})'
            }, status=400)
    
    # Crear test
    with transaction.atomic():
        test = Test(
            title=data.get('title'),
            description=data.get('description', ''),
            main_topic=main_topic,
            sub_topic=sub_topic,
            specific_topic=specific_topic,
            level=level,
            is_active=data.get('is_active', True),
            created_by=request.user,
        )
        test.save()
        
        # Crear preguntas y respuestas
        for q_data in questions_data:
            question = Question(
                test=test,
                question_text=q_data.get('question_text')
            )
            question.save()
            
            for a_data in q_data.get('answers', []):
                answer = Answer(
                    question=question,
                    answer_text=a_data.get('answer_text'),
                    is_correct=a_data.get('is_correct', False)
                )
                answer.save()
    
    # Invalidar cache
    invalidate_topics_cache()
    
    # Obtener test creado con relaciones
    created_test = Test.objects.prefetch_related('questions__answers').get(id=test.id)
    
    return JsonResponse({
        'test': test_to_dict(created_test),
        'message': 'Test creado exitosamente',
        'topics_cache_invalidated': True
    }, status=201)

@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
@admin_required
def update_test(request, test_id):
    """Actualizar un test existente"""
    # Verificar si el test existe
    try:
        existing_test = Test.objects.prefetch_related('questions__answers').get(id=test_id)
    except Test.DoesNotExist:
        return JsonResponse({'error': 'test no encontrado'}, status=404)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Validar nivel si se proporciona
    if 'level' in data and data['level']:
        valid_levels = get_predefined_levels()
        if data['level'] not in valid_levels:
            return JsonResponse({
                'error': 'Nivel no válido',
                'valid_levels': valid_levels
            }, status=400)
    
    # Actualizar temas
    main_topic = data.get('main_topic', existing_test.main_topic)
    sub_topic = data.get('sub_topic', existing_test.sub_topic)
    specific_topic = data.get('specific_topic', existing_test.specific_topic)
    
    try:
        insert_or_update_topic(main_topic, sub_topic, specific_topic, is_predefined=False)
        invalidate_topics_cache()
    except Exception as e:
        logger.warning(f"No se pudo guardar nuevo tema: {str(e)}")
    
    # Validar preguntas si se proporcionan
    if 'questions' in data and data['questions'] is not None:
        for i, question in enumerate(data['questions']):
            question_text = question.get('question_text', '').strip()
            question_id = question.get('id', 0)
            
            # Validar pregunta nueva sin texto
            if not question_text and question_id == 0:
                return JsonResponse({
                    'error': f'La nueva pregunta {i+1} no tiene texto'
                }, status=400)
            
            # Validar respuestas
            if 'answers' in question and question['answers']:
                answers = question['answers']
                
                # Para preguntas nuevas, validar al menos 2 respuestas
                if question_id == 0 and len(answers) < 2:
                    return JsonResponse({
                        'error': f'La nueva pregunta {i+1} debe tener al menos 2 respuestas'
                    }, status=400)
                
                # Validar exactamente una respuesta correcta
                correct_count = 0
                for j, answer in enumerate(answers):
                    answer_text = answer.get('answer_text', '').strip()
                    if not answer_text and answer.get('id', 0) == 0:
                        return JsonResponse({
                            'error': f'La nueva respuesta {j+1} de la pregunta {i+1} no tiene texto'
                        }, status=400)
                    if answer.get('is_correct', False):
                        correct_count += 1
                
                if correct_count != 1:
                    return JsonResponse({
                        'error': f'La pregunta {i+1} debe tener exactamente una respuesta correcta (tiene {correct_count})'
                    }, status=400)
    
    # Actualizar en transacción
    with transaction.atomic():
        # Actualizar campos básicos
        if 'title' in data:
            existing_test.title = data['title']
        if 'description' in data:
            existing_test.description = data['description']
        if 'main_topic' in data:
            existing_test.main_topic = data['main_topic']
        if 'sub_topic' in data:
            existing_test.sub_topic = data['sub_topic']
        if 'specific_topic' in data:
            existing_test.specific_topic = data['specific_topic']
        if 'level' in data:
            existing_test.level = data['level']
        if 'is_active' in data:
            existing_test.is_active = data['is_active']
        
        existing_test.updated_at = timezone.now()
        existing_test.save()
        
        # Procesar preguntas si se proporcionan
        if 'questions' in data and data['questions'] is not None:
            # Obtener IDs de preguntas existentes
            existing_question_ids = list(existing_test.questions.values_list('id', flat=True))
            
            for q_data in data['questions']:
                question_id = q_data.get('id', 0)
                
                if question_id == 0:
                    # Crear nueva pregunta
                    question = Question(
                        test=existing_test,
                        question_text=q_data.get('question_text')
                    )
                    question.save()
                    
                    # Crear respuestas
                    for a_data in q_data.get('answers', []):
                        Answer(
                            question=question,
                            answer_text=a_data.get('answer_text'),
                            is_correct=a_data.get('is_correct', False)
                        ).save()
                else:
                    # Actualizar pregunta existente
                    try:
                        question = Question.objects.get(id=question_id, test=existing_test)
                    except Question.DoesNotExist:
                        continue
                    
                    if q_data.get('question_text'):
                        question.question_text = q_data['question_text']
                        question.save()
                    
                    # Procesar respuestas
                    if 'answers' in q_data and q_data['answers']:
                        existing_answer_ids = list(question.answers.values_list('id', flat=True))
                        
                        for a_data in q_data['answers']:
                            answer_id = a_data.get('id', 0)
                            
                            if answer_id == 0:
                                # Nueva respuesta
                                Answer(
                                    question=question,
                                    answer_text=a_data.get('answer_text'),
                                    is_correct=a_data.get('is_correct', False)
                                ).save()
                            else:
                                # Actualizar respuesta existente
                                try:
                                    answer = Answer.objects.get(id=answer_id, question=question)
                                    if a_data.get('answer_text'):
                                        answer.answer_text = a_data['answer_text']
                                    answer.is_correct = a_data.get('is_correct', answer.is_correct)
                                    answer.save()
                                    
                                    # Remover de la lista de IDs existentes
                                    if answer_id in existing_answer_ids:
                                        existing_answer_ids.remove(answer_id)
                                except Answer.DoesNotExist:
                                    continue
                        
                        # Eliminar respuestas que no están en el input
                        for answer_id in existing_answer_ids:
                            Answer.objects.filter(id=answer_id).delete()
                    
                    # Remover de la lista de IDs existentes
                    if question_id in existing_question_ids:
                        existing_question_ids.remove(question_id)
            
            # Eliminar preguntas que no están en el input
            for question_id in existing_question_ids:
                # Las respuestas se eliminan en cascada por CASCADE en el modelo
                Question.objects.filter(id=question_id).delete()
    
    # Eliminar topics huérfanos
    try:
        rows_affected = delete_orphaned_topics()
        logger.info(f"Se eliminaron {rows_affected} topics huérfanos")
    except Exception as e:
        logger.warning(f"No se pudieron eliminar topics huérfanos: {str(e)}")
    
    # Invalidar cache
    invalidate_topics_cache()
    
    # Obtener test actualizado
    updated_test = Test.objects.prefetch_related('questions__answers').get(id=test_id)
    
    return JsonResponse({
        'test': test_to_dict(updated_test),
        'message': 'Test actualizado correctamente',
        'topics_cache_invalidated': True
    })

@require_http_methods(["DELETE"])
@admin_required
@csrf_exempt
def delete_test(request, test_id):
    """Eliminar un test"""
    try:
        test = Test.objects.get(id=test_id)
    except Test.DoesNotExist:
        return JsonResponse({'error': 'test no encontrado'}, status=404)
    
    # Eliminar en transacción
    with transaction.atomic():
        # 1. Eliminar resultados asociados
        Result.objects.filter(test_id=test_id).delete()
        
        # 2. Eliminar invitaciones
        TestInvitation.objects.filter(test_id=test_id).delete()
        
        # 3. Las preguntas y respuestas se eliminan en cascada por CASCADE
        test.delete()
    
    # Eliminar topics huérfanos
    try:
        rows_affected = delete_orphaned_topics()
        logger.info(f"Se eliminaron {rows_affected} topics huérfanos")
    except Exception as e:
        logger.warning(f"No se pudieron eliminar topics huérfanos: {str(e)}")
    
    # Invalidar cache
    invalidate_topics_cache()
    
    return JsonResponse({
        'message': 'Test eliminado correctamente',
        'topics_cache_invalidated': True
    })


@require_http_methods(["GET"])
@admin_required
def get_all_tests(request):
    """Obtener todos los tests con paginación, filtrado y ordenación"""
    # Obtener parámetros de consulta
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    sort_by = request.GET.get('sort_by', 'created_at')
    sort_order = request.GET.get('sort_order', 'desc')
    main_topic = request.GET.get('main_topic', '')
    sub_topic = request.GET.get('sub_topic', '')
    level = request.GET.get('level', '')
    is_active_param = request.GET.get('is_active')
    search = request.GET.get('search', '')
    
    # Validaciones
    if page < 1:
        page = 1
    if page_size < 1 or page_size > 100:
        page_size = 10
    
    valid_sort_fields = ['id', 'title', 'main_topic', 'sub_topic', 'level', 'is_active', 'updated_at', 'created_at', 'created_by']
    if sort_by not in valid_sort_fields:
        sort_by = 'created_at'
    
    if sort_order not in ['asc', 'desc']:
        sort_order = 'desc'
    
    # Construir consulta base con conteo de preguntas
    query = Test.objects.annotate(question_count=Count('questions'))
    
    # Contar total sin filtros
    total_tests = Test.objects.count()
    
    # Aplicar filtros
    if main_topic:
        query = query.filter(main_topic=main_topic)
    
    if sub_topic:
        query = query.filter(sub_topic=sub_topic)
    
    if level:
        query = query.filter(level=level)
    
    if is_active_param is not None:
        is_active = is_active_param.lower() == 'true'
        query = query.filter(is_active=is_active)
    
    if search:
        query = query.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    
    # Contar total filtrado
    total_filtered_tests = query.count()
    
    # Aplicar ordenación
    if sort_order == 'desc':
        sort_by = f'-{sort_by}'
    query = query.order_by(sort_by)
    
    # Aplicar paginación
    offset = (page - 1) * page_size
    tests = query[offset:offset + page_size]
    
    # Obtener filtros disponibles
    main_topics = get_main_topics()
    sub_topics = get_sub_topics(main_topic) if main_topic else []
    levels = get_predefined_levels()
    statuses = ['Activo', 'Inactivo']
    
    # Construir respuesta
    tests_data = []
    for test in tests:
        test_dict = test_to_dict(test)
        test_dict['question_count'] = test.question_count
        tests_data.append(test_dict)
    
    return JsonResponse({
        'tests': tests_data,
        'filters_applied': {
            'page': page,
            'page_size': page_size,
            'main_topic': main_topic,
            'sub_topic': sub_topic,
            'level': level,
            'is_active': is_active_param,
            'search': search,
            'sort_by': sort_by.lstrip('-') if sort_by.startswith('-') else sort_by,
            'sort_order': sort_order
        },
        'available_filters': {
            'main_topics': main_topics,
            'sub_topics': sub_topics,
            'levels': levels,
            'statuses': statuses,
            'roles': ['user', 'admin']
        },
        'stats': {
            'total_tests': total_tests,
            'total_filtered_tests': total_filtered_tests
        }
    })


@require_http_methods(["GET"])
@admin_required
def get_test_by_id(request, test_id):
    """Obtener test por ID con preguntas y respuestas"""
    try:
        test = Test.objects.prefetch_related('questions__answers').get(id=test_id)
    except Test.DoesNotExist:
        return JsonResponse({'error': 'test no encontrado'}, status=404)
    
    return JsonResponse({'test': test_to_dict(test)})

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
        'created_by': test.created_by.id,       
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



# ====== Vistas de Usuarios ======

@require_http_methods(["GET"])
@admin_required
def get_user_by_id(request, user_id):
    """Obtener usuario por ID"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'usuario no encontrado'}, status=404)
    
    return JsonResponse({'user': user_to_response(user)})

@require_http_methods(["GET"])
@admin_required
def get_user_profile(request, user_id):
    """Obtener datos básicos de perfil de usuario"""
    try:
        user = User.objects.values(
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'address', 'country', 'birth_date', 'role',
            'registered_at', 'login_at'
        ).get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'usuario no encontrado'}, status=404)
    
    # Formatear fechas
    if user['birth_date']:
        user['birth_date'] = user['birth_date'].isoformat()
    if user['registered_at']:
        user['registered_at'] = user['registered_at'].isoformat()
    if user['login_at']:
        user['login_at'] = user['login_at'].isoformat()
    
    return JsonResponse({'user': user})

@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
@admin_required
def update_user(request, user_id):
    """Actualizar usuario"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'usuario no encontrado'}, status=404)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Actualizar campos
    if 'first_name' in data and data['first_name']:
        user.first_name = data['first_name']
    if 'last_name' in data and data['last_name']:
        user.last_name = data['last_name']
    if 'email' in data and data['email']:
        user.email = data['email']
    if 'phone' in data:
        user.phone = data['phone']
    if 'address' in data:
        user.address = data['address']
    if 'country' in data:
        user.country = data['country']
    if 'birth_date' in data and data['birth_date']:
        try:
            user.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'formato de fecha inválido. Use YYYY-MM-DD'}, status=400)
    if 'role' in data and data['role'] in ['user', 'admin']:
        user.role = data['role']
    
    try:
        user.save()
    except Exception as e:
        return JsonResponse({'error': f'error al actualizar usuario: {str(e)}'}, status=500)
    
    return JsonResponse({
        'user': user_to_response(user),
        'message': 'Usuario actualizado correctamente'
    })


@require_http_methods(["GET"])
@admin_required
def get_users_with_stats(request):
    """Obtener usuarios con estadísticas completas (con paginación, filtrado y ordenación)"""
    # Obtener parámetros de consulta
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    sort_by = request.GET.get('sort_by', 'registered_at')
    sort_order = request.GET.get('sort_order', 'desc')
    role = request.GET.get('role', '')
    search = request.GET.get('search', '')
    
    # Validaciones
    if page < 1:
        page = 1
    if page_size < 1 or page_size > 100:
        page_size = 10
    
    valid_sort_fields = ['id', 'username', 'email', 'role', 'registered_at', 
                         'login_at', 'tests_completed', 'average_score']
    if sort_by not in valid_sort_fields:
        sort_by = 'registered_at'
    
    if sort_order not in ['asc', 'desc']:
        sort_order = 'desc'
    
    # Contar total de usuarios
    total_users = User.objects.count()
       
    # Anotaciones para estadísticas
    users_with_stats = User.objects.annotate(
        # Tests completados
        tests_completed=Coalesce(
            Count('results', filter=Q(results__status='completed')),
            Value(0)
        ),
        # Tests en progreso
        tests_in_progress=Coalesce(
            Count('results', filter=Q(results__status='in_progress')),
            Value(0)
        ),
        # Puntuación media (solo tests completados)
        average_score=Coalesce(
            Avg(
                Case(
                    When(
                        results__status='completed',
                        then=Cast(
                            F('results__correct_answers') * 100.0 /
                            (F('results__correct_answers') + F('results__wrong_answers')),
                            FloatField()
                        )
                    ),
                    default=None
                )
            ),
            Value(0.0)
        ),

        # Total de tests realizados
        total_tests_taken=Coalesce(Count('results'), Value(0))
    )
    
    # Aplicar filtros
    if role:
        users_with_stats = users_with_stats.filter(role=role)
    
    if search:
        users_with_stats = users_with_stats.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    # Contar total filtrado
    total_filtered_users = users_with_stats.count()
    
    # Calcular tests_no_iniciados (total de tests - tests realizados)
    from apps.test.models import Test
    total_tests_count = Test.objects.count()
    
    # Obtener usuarios con valores calculados adicionales
    users_list = list(users_with_stats)
    
    for user in users_list:
        # Calcular tests no iniciados
        user.tests_not_started = total_tests_count - user.total_tests_taken
        
        # Formatear fechas para JSON
        user.birth_date_str = user.birth_date.isoformat() if user.birth_date else None
        user.registered_at_str = user.registered_at.isoformat() if user.registered_at else None
        user.login_at_str = user.login_at.isoformat() if user.login_at else None
    
    # Ordenar
    reverse = (sort_order == 'desc')
    if sort_by == 'tests_completed':
        users_list.sort(key=lambda x: x.tests_completed, reverse=reverse)
    elif sort_by == 'average_score':
        users_list.sort(key=lambda x: x.average_score if x.average_score else 0, reverse=reverse)
    elif sort_by == 'registered_at':
        users_list.sort(key=lambda x: x.registered_at or datetime.min, reverse=reverse)
    elif sort_by == 'login_at':
        users_list.sort(key=lambda x: x.login_at or datetime.min, reverse=reverse)
    else:
        users_list.sort(key=lambda x: getattr(x, sort_by, ''), reverse=reverse)
    
    # Paginar
    start = (page - 1) * page_size
    end = start + page_size
    paginated_users = users_list[start:end]
    
    # Construir respuesta
    users_data = []
    for user in paginated_users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'address': user.address,
            'country': user.country,
            'birth_date': user.birth_date_str,
            'role': user.role,
            'registered_at': user.registered_at_str,
            'login_at': user.login_at_str,
            'tests_completed': user.tests_completed,
            'tests_in_progress': user.tests_in_progress,
            'tests_not_started': user.tests_not_started,
            'average_score': round(user.average_score, 2) if user.average_score else 0,
            'total_tests_taken': user.total_tests_taken,
        })
    
    return JsonResponse({
        'users': users_data,
        'stats': {
            'total_users': total_users,
            'total_filtered_users': total_filtered_users,
        },
        'filters': {
            'page': page,
            'page_size': page_size,
            'role': role,
            'search': search,
            'sort_by': sort_by,
            'sort_order': sort_order,
        }
    })


@csrf_exempt
@require_http_methods(["DELETE"])
@admin_required
def delete_user(request, user_id):
    """Elimina permanentemente un usuario y transfiere sus tests al usuario ID=1"""
    user_id = int(user_id)
    
    # Verificar que no se intente eliminar al usuario ID=1
    if user_id == 1:
        return JsonResponse({
            'error': 'No se puede eliminar el usuario administrador principal (ID=1)'
        }, status=400)
    
    # Buscar usuario (incluyendo soft-deleted si usas soft delete)
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'usuario no encontrado'}, status=404)
    
    # Verificar si es administrador y prevenir eliminación del único admin
    if user.role == 'admin':
        admin_count = User.objects.filter(role='admin', is_active=True).count()
        
        # Si es el único administrador activo, no permitir eliminar
        if admin_count <= 1:
            return JsonResponse({
                'error': 'No se puede eliminar el único administrador activo del sistema'
            }, status=400)
    
    # Verificar que el usuario destino (ID=1) existe
    try:
        target_user = User.objects.get(id=1)
    except User.DoesNotExist:
        return JsonResponse({
            'error': 'El usuario destino para transferencia (ID=1) no existe'
        }, status=500)
    
    # Ejecutar transacción para eliminación permanente con transferencia
    try:
        with transaction.atomic():
            # 1. Eliminar tokens de restablecimiento de contraseña
            PasswordResetToken.objects.filter(user_id=user_id).delete()
            
            # 2. Transferir tests al usuario ID=1
            from ..admin_panel.models import Test
            Test.objects.filter(created_by=user_id).update(created_by=1)
            
            # 3. Transferir resultados al usuario ID=1
            Result.objects.filter(user_id=user_id).update(user_id=1)
            
            # 4. Eliminar quotas del usuario (si existen)
            # UserQuota.objects.filter(user_id=user_id).delete()
            
            # 5. Eliminar invitaciones ENVIADAS por el usuario
            TestInvitation.objects.filter(invited_by_id=user_id).delete()
            
            # 6. Limpiar referencia en invitaciones RECIBIDAS (si el usuario era guest)
            TestInvitation.objects.filter(guest_user_id=user_id).update(guest_user=None)
            
            # 7. Eliminar permanentemente al usuario
            user.delete()
        
        return JsonResponse({
            'message': 'Usuario eliminado permanentemente',
            'deleted_user_id': user_id,
            'deleted_username': user.username,
            'transferred_to_user': 1,
            'transferred_to_email': target_user.email
        })
        
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

# Funciones auxiliares
def user_to_response(user):
    """Convierte un objeto User a diccionario de respuesta"""
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone': user.phone,
        'address': user.address,
        'country': user.country,
        'birth_date': user.birth_date.isoformat() if user.birth_date else None,
        'role': user.role,
        'registered_at': user.registered_at.isoformat() if user.registered_at else None,
        'login_at': user.login_at.isoformat() if user.login_at else None,
    }



# ====== Vistas de Resultados ======


@require_http_methods(["GET"])
@admin_required
def get_result_stats(request):
    """Obtener estadísticas generales de resultados"""
    
    # Estadísticas básicas
    total_results = Result.objects.count()
    
    # Resultados por estado
    status_stats = Result.objects.values('status').annotate(count=Count('id'))
    
    # Puntuación media general
    avg_score = Result.objects.filter(status='completed').annotate(
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
    ).aggregate(avg_score=Avg('score'))['avg_score'] or 0
    
    # Resultados por día (últimos 30 días)
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    daily_stats = Result.objects.filter(
        started_at__gte=thirty_days_ago
    ).extra(
        {'day': "DATE(started_at)"}
    ).values('day').annotate(
        count=Count('id'),
        avg_score=Avg(
            Case(
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
    ).order_by('day')
    
    # Resultados por nivel de test
    level_stats = Result.objects.select_related('test').values('test__level').annotate(
        count=Count('id'),
        avg_score=Avg(
            Case(
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
    )
    
    # Top 10 tests más realizados
    top_tests = Result.objects.select_related('test').values(
        'test__id', 'test__title'
    ).annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Top 10 usuarios con más resultados
    top_users = Result.objects.select_related('user').values(
        'user__id', 'user__username', 'user__email'
    ).annotate(
        count=Count('id'),
        avg_score=Avg(
            Case(
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
    ).order_by('-count')[:10]
    
    return JsonResponse({
        'stats': {
            'total_results': total_results,
            'average_score': round(float(avg_score), 2),
            'by_status': list(status_stats),
            'by_level': list(level_stats),
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
    })

@require_http_methods(["GET"])
@admin_required
def get_result_detail(request, result_id):
    """Obtener detalle completo de un resultado"""
    try:
        result = Result.objects.select_related('user', 'test').get(id=result_id)
    except Result.DoesNotExist:
        return JsonResponse({'error': 'Resultado no encontrado'}, status=404)
    
    # Calcular score
    total_answered = result.correct_answers + result.wrong_answers
    score = 0
    if result.status == 'completed' and total_answered > 0:
        score = round((result.correct_answers * 100.0 / total_answered), 2)
    
    # Parsear respuestas si están almacenadas como JSON
    answers_data = None
    if result.answers:
        try:
            answers_data = json.loads(result.answers) if isinstance(result.answers, str) else result.answers
        except json.JSONDecodeError:
            answers_data = result.answers
    
    response_data = {
        'id': result.id,
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
    }
    
    return JsonResponse(response_data)

@require_http_methods(["GET"])
@admin_required
def export_results_csv(request):
    """Exportar resultados a CSV (opcional)"""
    import csv
    
    # Obtener filtros de la consulta
    # (Similar a get_results_list pero sin paginación)
    
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
    )
    
    # Aplicar filtros (similar a get_results_list)
    # ... (copiar la lógica de filtros)
    
    # Crear respuesta CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="results_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Usuario', 'Email', 'Test', 'Nivel', 'Tema Principal',
        'Subtema', 'Correctas', 'Incorrectas', 'Total', 'Puntuación (%)',
        'Tiempo (seg)', 'Estado', 'Fecha Inicio', 'Última Actualización'
    ])
    
    for result in results_query:
        writer.writerow([
            result.id,
            result.user.username,
            result.user.email,
            result.test.title,
            result.test.level,
            result.test.main_topic,
            result.test.sub_topic,
            result.correct_answers,
            result.wrong_answers,
            result.total_questions,
            result.score,
            result.time_taken,
            result.status,
            result.started_at.isoformat() if result.started_at else '',
            result.updated_at.isoformat() if result.updated_at else '',
        ])
    
    return response




# ====== Vistas de Invitaciones ======

@require_http_methods(["GET"])
@admin_required
def admin_get_invitations(request):
    """Obtener todas las invitaciones con filtros y paginación"""
    
    # Obtener parámetros de consulta
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    sort_by = request.GET.get('sort_by', 'created_at')
    sort_order = request.GET.get('sort_order', 'desc')
    
    # Filtros
    search = request.GET.get('search', '')
    test_id = request.GET.get('test_id')
    invited_by = request.GET.get('invited_by')
    is_used_param = request.GET.get('is_used')
    is_guest_param = request.GET.get('is_guest')
    status = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Validaciones
    if page < 1:
        page = 1
    if page_size < 1 or page_size > 100:
        page_size = 20
    
    valid_sort_fields = ['id', 'test_id', 'invited_by', 'is_used', 'is_guest', 
                         'expires_at', 'created_at']
    if sort_by not in valid_sort_fields:
        sort_by = 'created_at'
    
    if sort_order not in ['asc', 'desc']:
        sort_order = 'desc'
    
    # Construir consulta base con selección relacionada
    query = TestInvitation.objects.select_related('test', 'invited_by', 'guest_user')
    
    # Aplicar filtros
    if search:
        query = query.filter(
            Q(message__icontains=search) | Q(token__icontains=search)
        )
    
    if test_id:
        try:
            query = query.filter(test_id=int(test_id))
        except ValueError:
            pass
    
    if invited_by:
        try:
            query = query.filter(invited_by_id=int(invited_by))
        except ValueError:
            pass
    
    if is_used_param is not None:
        is_used = is_used_param.lower() == 'true'
        query = query.filter(is_used=is_used)
    
    if is_guest_param is not None:
        is_guest = is_guest_param.lower() == 'true'
        query = query.filter(is_guest=is_guest)
    
    # Filtrar por estado
    now = timezone.now()
    if status:
        if status == 'active':
            query = query.filter(is_used=False, expires_at__gt=now)
        elif status == 'used':
            query = query.filter(is_used=True)
        elif status == 'expired':
            query = query.filter(expires_at__lte=now)
    
    # Filtrar por fechas
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(created_at__date__gte=start)
        except ValueError:
            pass
    
    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(created_at__date__lte=end)
        except ValueError:
            pass
    
    # Contar total (sin filtros)
    total_invitations = TestInvitation.objects.count()
    
    # Contar total filtrado
    total_filtered = query.count()
    
    # Aplicar ordenación
    if sort_order == 'desc':
        sort_by = f'-{sort_by}'
    query = query.order_by(sort_by)
    
    # Paginar
    paginator = Paginator(query, page_size)
    page_obj = paginator.get_page(page)
    
    # Construir respuesta
    invitations_data = []
    for inv in page_obj:
        # Determinar estado
        if inv.is_used:
            inv_status = 'used'
        elif inv.expires_at < timezone.now():
            inv_status = 'expired'
        else:
            inv_status = 'active'
        
        invitation_dict = {
            'id': inv.id,
            'test_id': inv.test.id,
            'test_title': inv.test.title,
            'invited_by': inv.invited_by.id,
            'inviter_name': inv.invited_by.username,
            'message': inv.message,
            'token': inv.token,
            'is_used': inv.is_used,
            'is_guest': inv.is_guest,
            'guest_user_id': inv.guest_user.id if inv.guest_user else None,
            'guest_name': inv.guest_user.username if inv.guest_user else None,
            'expires_at': inv.expires_at.isoformat(),
            'created_at': inv.created_at.isoformat(),
            'status': inv_status,
            'invitation_url': inv.invitation_url,
        }
        invitations_data.append(invitation_dict)
    
    return JsonResponse({
        'invitations': invitations_data,
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total_items': total_filtered,
            'total_pages': paginator.num_pages,
        },
        'filters_applied': {
            'page': page,
            'page_size': page_size,
            'sort_by': sort_by.lstrip('-') if sort_by.startswith('-') else sort_by,
            'sort_order': sort_order,
            'search': search,
            'test_id': test_id,
            'invited_by': invited_by,
            'is_used': is_used_param,
            'is_guest': is_guest_param,
            'status': status,
            'start_date': start_date,
            'end_date': end_date,
        },
        'available_filters': {
            'total_invitations': total_invitations,
        }
    })


@csrf_exempt
@require_http_methods(["DELETE"])
@admin_required
def admin_delete_invitation(request, invitation_id):
    """Eliminar una invitación específica"""
    try:
        invitation = TestInvitation.objects.get(id=invitation_id)
    except TestInvitation.DoesNotExist:
        return JsonResponse({'error': 'invitación no encontrada'}, status=404)
    
    # Verificar si está usada
    if invitation.is_used:
        return JsonResponse({
            'error': 'no se puede eliminar una invitación usada'
        }, status=400)
    
    invitation.delete()
    
    return JsonResponse({
        'message': 'Invitación eliminada exitosamente',
        'id': invitation_id
    })

@csrf_exempt
@require_http_methods(["POST"])
@admin_required
def admin_delete_invitations_bulk(request):
    """Eliminar múltiples invitaciones"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    ids = data.get('ids', [])
    if not ids or not isinstance(ids, list) or len(ids) < 1:
        return JsonResponse({
            'error': 'Se requiere una lista de IDs con al menos un elemento'
        }, status=400)
    
    # Validar que todos los IDs sean enteros
    try:
        ids = [int(id_val) for id_val in ids]
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Los IDs deben ser números enteros'}, status=400)
    
    # Verificar que ninguna invitación esté usada
    used_count = TestInvitation.objects.filter(id__in=ids, is_used=True).count()
    if used_count > 0:
        return JsonResponse({
            'error': 'una o más invitaciones ya están usadas y no pueden ser eliminadas'
        }, status=400)
    
    # Eliminar en lote
    deleted_count, _ = TestInvitation.objects.filter(id__in=ids).delete()
    
    return JsonResponse({
        'message': 'Invitaciones eliminadas exitosamente',
        'deleted_count': deleted_count,
        'deleted_ids': ids
    })

@require_http_methods(["GET"])
@admin_required
def admin_get_invitation_stats(request):
    """Obtener estadísticas de invitaciones"""
    now = timezone.now()
    
    # Estadísticas básicas
    stats = {
        'total': TestInvitation.objects.count(),
        'active': TestInvitation.objects.filter(
            is_used=False, expires_at__gt=now
        ).count(),
        'used': TestInvitation.objects.filter(is_used=True).count(),
        'expired': TestInvitation.objects.filter(expires_at__lte=now).count(),
        'with_guest': TestInvitation.objects.filter(guest_user__isnull=False).count(),
    }
    
    # Estadísticas por test
    test_stats = TestInvitation.objects.values(
        'test__id', 'test__title'
    ).annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Estadísticas por usuario que invita
    user_stats = TestInvitation.objects.values(
        'invited_by__id', 'invited_by__username', 'invited_by__email'
    ).annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Estadísticas por día (últimos 30 días)
    thirty_days_ago = now - timezone.timedelta(days=30)
    daily_stats = TestInvitation.objects.filter(
        created_at__gte=thirty_days_ago
    ).extra(
        {'day': "DATE(created_at)"}
    ).values('day').annotate(
        count=Count('id')
    ).order_by('day')
    
    # Estadísticas por estado a lo largo del tiempo
    status_over_time = {
        'last_7_days': [],
        'last_30_days': [],
    }
    
    # Últimos 7 días
    seven_days_ago = now - timezone.timedelta(days=7)
    last_7_days = TestInvitation.objects.filter(
        created_at__gte=seven_days_ago
    ).extra(
        {'day': "DATE(created_at)"}
    ).values('day').annotate(
        total=Count('id'),
        active=Count('id', filter=Q(is_used=False, expires_at__gt=now)),
        used=Count('id', filter=Q(is_used=True)),
        expired=Count('id', filter=Q(expires_at__lte=now)),
    ).order_by('day')
    
    for item in last_7_days:
        status_over_time['last_7_days'].append({
            'date': item['day'].isoformat() if item['day'] else None,
            'total': item['total'],
            'active': item['active'],
            'used': item['used'],
            'expired': item['expired'],
        })
    
    # Últimos 30 días
    last_30_days = TestInvitation.objects.filter(
        created_at__gte=thirty_days_ago
    ).extra(
        {'day': "DATE(created_at)"}
    ).values('day').annotate(
        total=Count('id'),
        active=Count('id', filter=Q(is_used=False, expires_at__gt=now)),
        used=Count('id', filter=Q(is_used=True)),
        expired=Count('id', filter=Q(expires_at__lte=now)),
    ).order_by('day')
    
    for item in last_30_days:
        status_over_time['last_30_days'].append({
            'date': item['day'].isoformat() if item['day'] else None,
            'total': item['total'],
            'active': item['active'],
            'used': item['used'],
            'expired': item['expired'],
        })
    
    return JsonResponse({
        'stats': stats,
        'by_test': list(test_stats),
        'by_user': list(user_stats),
        'daily_last_30_days': [
            {
                'date': item['day'].isoformat() if item['day'] else None,
                'count': item['count']
            }
            for item in daily_stats
        ],
        'status_over_time': status_over_time,
        'timestamp': now.isoformat()
    })

@require_http_methods(["GET"])
@admin_required
def admin_get_invitation_detail(request, invitation_id):
    """Obtener detalle completo de una invitación"""
    try:
        invitation = TestInvitation.objects.select_related(
            'test', 'invited_by', 'guest_user'
        ).get(id=invitation_id)
    except TestInvitation.DoesNotExist:
        return JsonResponse({'error': 'invitación no encontrada'}, status=404)
    
    # Determinar estado
    now = timezone.now()
    if invitation.is_used:
        status = 'used'
    elif invitation.expires_at < now:
        status = 'expired'
    else:
        status = 'active'
    
    # Obtener estadísticas adicionales si la invitación tiene guest user
    guest_stats = None
    if invitation.guest_user:
        from ..results.models import Result
        results_count = Result.objects.filter(user=invitation.guest_user).count()
        completed_results = Result.objects.filter(
            user=invitation.guest_user, status='completed'
        ).count()
        
        guest_stats = {
            'total_tests_taken': results_count,
            'completed_tests': completed_results,
        }
    
    response_data = {
        'id': invitation.id,
        'test': {
            'id': invitation.test.id,
            'title': invitation.test.title,
            'description': invitation.test.description,
            'main_topic': invitation.test.main_topic,
            'sub_topic': invitation.test.sub_topic,
            'specific_topic': invitation.test.specific_topic,
            'level': invitation.test.level,
            'total_questions': invitation.test.questions.count(),
        },
        'inviter': {
            'id': invitation.invited_by.id,
            'username': invitation.invited_by.username,
            'email': invitation.invited_by.email,
            'first_name': invitation.invited_by.first_name,
            'last_name': invitation.invited_by.last_name,
        },
        'guest_user': {
            'id': invitation.guest_user.id,
            'username': invitation.guest_user.username,
            'email': invitation.guest_user.email,
            'first_name': invitation.guest_user.first_name,
            'last_name': invitation.guest_user.last_name,
        } if invitation.guest_user else None,
        'guest_stats': guest_stats,
        'message': invitation.message,
        'token': invitation.token,
        'is_used': invitation.is_used,
        'is_guest': invitation.is_guest,
        'expires_at': invitation.expires_at.isoformat(),
        'created_at': invitation.created_at.isoformat(),
        'status': status,
        'invitation_url': invitation.invitation_url,
        'time_until_expiry': None,
        'time_since_created': None,
    }
    
    # Calcular tiempos
    if status == 'active':
        time_until = invitation.expires_at - now
        response_data['time_until_expiry'] = {
            'days': time_until.days,
            'hours': time_until.seconds // 3600,
            'minutes': (time_until.seconds % 3600) // 60,
        }
    
    time_since = now - invitation.created_at
    response_data['time_since_created'] = {
        'days': time_since.days,
        'hours': time_since.seconds // 3600,
        'minutes': (time_since.seconds % 3600) // 60,
    }
    
    return JsonResponse(response_data)



# ====== Vistas de Cuotas de Usuario ======

@require_http_methods(["GET"])
@admin_required
def admin_get_user_quotas(request):
    """Obtener todas las cuotas de usuarios con filtros y paginación"""
    
    # Obtener parámetros de consulta
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    sort_by = request.GET.get('sort_by', 'month_year')
    sort_order = request.GET.get('sort_order', 'desc')
    
    # Filtros
    search = request.GET.get('search', '')
    user_id = request.GET.get('user_id')
    month_year = request.GET.get('month_year')
    min_remaining = request.GET.get('min_remaining')
    max_usage = request.GET.get('max_usage')
    min_requests = request.GET.get('min_requests')
    max_requests = request.GET.get('max_requests')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Validaciones
    if page < 1:
        page = 1
    if page_size < 1 or page_size > 100:
        page_size = 20
    
    valid_sort_fields = ['id', 'user_id', 'month_year', 'max_requests', 
                         'used_requests', 'created_at', 'updated_at']
    if sort_by not in valid_sort_fields:
        sort_by = 'month_year'
    
    if sort_order not in ['asc', 'desc']:
        sort_order = 'desc'
    
    # Contar total global
    global_total = UserQuota.objects.count()
    
    # Construir consulta base con selección relacionada
    query = UserQuota.objects.select_related('user')
    
    # Aplicar filtros
    if search:
        query = query.filter(
            Q(user__username__icontains=search) |
            Q(user__email__icontains=search) |
            Q(user__id__icontains=search)
        )
    
    if user_id:
        try:
            query = query.filter(user_id=int(user_id))
        except ValueError:
            pass
    
    if month_year:
        query = query.filter(month_year=month_year)
    
    # Filtrar por solicitudes restantes mínimas
    if min_remaining:
        try:
            min_rem = int(min_remaining)
            # remaining = max_requests - used_requests
            query = query.filter(
                F('max_requests') - F('used_requests') >= min_rem
            )
        except ValueError:
            pass
    
    # Filtrar por porcentaje de uso máximo
    if max_usage:
        try:
            max_usage_val = int(max_usage)
            query = query.filter(
                max_requests__gt=0
            ).extra(
                where=["(used_requests * 100 / max_requests) <= %s"],
                params=[max_usage_val]
            )
        except ValueError:
            pass
    
    # Filtrar por rango de solicitudes máximas
    if min_requests:
        try:
            query = query.filter(max_requests__gte=int(min_requests))
        except ValueError:
            pass
    
    if max_requests:
        try:
            query = query.filter(max_requests__lte=int(max_requests))
        except ValueError:
            pass
    
    # Filtrar por fechas
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(created_at__date__gte=start)
        except ValueError:
            pass
    
    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(created_at__date__lte=end)
        except ValueError:
            pass
    
    # Contar total filtrado
    filtered_total = query.count()
    
    # Aplicar ordenación
    if sort_order == 'desc':
        sort_by = f'-{sort_by}'
    query = query.order_by(sort_by)
    
    # Paginar
    paginator = Paginator(query, page_size)
    page_obj = paginator.get_page(page)
    
    # Construir respuesta
    quotas_data = []
    for quota in page_obj:
        quota_dict = {
            'id': quota.id,
            'user_id': quota.user.id,
            'username': quota.user.username,
            'user_email': quota.user.email,
            'month_year': quota.month_year,
            'max_requests': quota.max_requests,
            'used_requests': quota.used_requests,
            'remaining_requests': quota.remaining_requests,
            'usage_percentage': quota.usage_percentage,
            'status': quota.status,
            'created_at': quota.created_at.isoformat(),
            'updated_at': quota.updated_at.isoformat(),
        }
        quotas_data.append(quota_dict)
    
    # Obtener meses disponibles para filtros
    available_months = UserQuota.objects.values_list('month_year', flat=True)\
        .distinct().order_by('-month_year')[:12]
    
    if not available_months:
        available_months = [datetime.now().strftime('%Y-%m')]
    
    return JsonResponse({
        'quotas': quotas_data,
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total_items': filtered_total,
            'total_pages': paginator.num_pages,
        },
        'filters_applied': {
            'page': page,
            'page_size': page_size,
            'sort_by': sort_by.lstrip('-') if sort_by.startswith('-') else sort_by,
            'sort_order': sort_order,
            'search': search,
            'user_id': user_id,
            'month_year': month_year,
            'min_remaining': min_remaining,
            'max_usage': max_usage,
            'min_requests': min_requests,
            'max_requests': max_requests,
            'start_date': start_date,
            'end_date': end_date,
        },
        'available_filters': {
            'total_quotas': global_total,
            'filtered_quotas': filtered_total,
            'available_months': list(available_months),
            'available_statuses': ['normal', 'warning', 'critical', 'exceeded'],
            'default_max_requests': 5,
        }
    })

@require_http_methods(["GET"])
@admin_required
def admin_get_user_quota(request, user_id):
    """Obtener cuota de un usuario específico"""
    month_year = request.GET.get('month_year')
    
    query = UserQuota.objects.select_related('user').filter(user_id=user_id)
    
    if month_year:
        query = query.filter(month_year=month_year)
    else:
        query = query.order_by('-month_year')
    
    try:
        quota = query.first()
        if not quota:
            return JsonResponse({'error': 'cuota no encontrada'}, status=404)
    except UserQuota.DoesNotExist:
        return JsonResponse({'error': 'cuota no encontrada'}, status=404)
    
    quota_data = {
        'id': quota.id,
        'user_id': quota.user.id,
        'username': quota.user.username,
        'user_email': quota.user.email,
        'month_year': quota.month_year,
        'max_requests': quota.max_requests,
        'used_requests': quota.used_requests,
        'remaining_requests': quota.remaining_requests,
        'usage_percentage': quota.usage_percentage,
        'status': quota.status,
        'created_at': quota.created_at.isoformat(),
        'updated_at': quota.updated_at.isoformat(),
    }
    
    return JsonResponse({'quota': quota_data})

@require_http_methods(["GET"])
@admin_required
def admin_get_quota_stats(request):
    """Obtener estadísticas globales de cuotas"""
    
    # Estadísticas básicas
    stats = {
        'total_users_with_quota': UserQuota.objects.values('user_id').distinct().count(),
        'total_requests_allowed': UserQuota.objects.aggregate(total=Sum('max_requests'))['total'] or 0,
        'total_requests_used': UserQuota.objects.aggregate(total=Sum('used_requests'))['total'] or 0,
    }
    
    # Usuarios que han excedido su cuota
    stats['users_exceeding_quota'] = UserQuota.objects.filter(
        used_requests__gt=F('max_requests')
    ).values('user_id').distinct().count()
    
    # Usuarios en estado crítico (uso >= 80% y <= 100%)
    stats['users_critical'] = UserQuota.objects.filter(
        max_requests__gt=0
    ).extra(
        where=["(used_requests * 100 / max_requests) >= 80"],
        having=["(used_requests * 100 / max_requests) <= 100"]
    ).values('user_id').distinct().count()
    
    # Usuarios en estado de advertencia (uso >= 50% y < 80%)
    stats['users_warning'] = UserQuota.objects.filter(
        max_requests__gt=0
    ).extra(
        where=["(used_requests * 100 / max_requests) >= 50"],
        having=["(used_requests * 100 / max_requests) < 80"]
    ).values('user_id').distinct().count()
    
    # Datos del mes actual
    current_month = datetime.now().strftime('%Y-%m')
    current_month_quota = UserQuota.objects.filter(month_year=current_month).aggregate(
        total_requests=Sum('max_requests'),
        used_requests=Sum('used_requests')
    )
    
    # Distribución por mes
    monthly_stats = UserQuota.objects.values('month_year').annotate(
        total_requests=Sum('max_requests'),
        used_requests=Sum('used_requests'),
        user_count=Count('user_id', distinct=True)
    ).order_by('-month_year')[:12]
    
    # Top usuarios con mayor uso
    top_users = UserQuota.objects.select_related('user').values(
        'user_id', 'user__username', 'user__email'
    ).annotate(
        total_used=Sum('used_requests'),
        total_allowed=Sum('max_requests')
    ).order_by('-total_used')[:10]
    
    return JsonResponse({
        'stats': stats,
        'current_month': {
            'month': current_month,
            'total_requests': current_month_quota['total_requests'] or 0,
            'used_requests': current_month_quota['used_requests'] or 0,
        },
        'monthly_stats': [
            {
                'month': item['month_year'],
                'total_requests': item['total_requests'] or 0,
                'used_requests': item['used_requests'] or 0,
                'user_count': item['user_count'],
                'usage_percentage': int((item['used_requests'] or 0) * 100 / (item['total_requests'] or 1))
            }
            for item in monthly_stats
        ],
        'top_users': [
            {
                'user_id': item['user_id'],
                'username': item['user__username'],
                'email': item['user__email'],
                'total_used': item['total_used'],
                'total_allowed': item['total_allowed'],
                'usage_percentage': int(item['total_used'] * 100 / (item['total_allowed'] or 1))
            }
            for item in top_users
        ],
        'timestamp': datetime.now().isoformat()
    })

@require_http_methods(["GET"])
@admin_required
def admin_get_user_quota_months(request, user_id):
    """Obtener los meses disponibles para un usuario"""
    months = UserQuota.objects.filter(user_id=user_id)\
        .values_list('month_year', flat=True)\
        .distinct()\
        .order_by('-month_year')
    
    return JsonResponse({'months': list(months)})

@csrf_exempt
@require_http_methods(["POST"])
@admin_required
def admin_create_user_quota(request):
    """Crear una nueva cuota para un usuario"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Validar campos requeridos
    required_fields = ['user_id', 'month_year', 'max_requests']
    for field in required_fields:
        if field not in data:
            return JsonResponse({'error': f'{field} is required'}, status=400)
    
    user_id = data.get('user_id')
    month_year = data.get('month_year')
    max_requests = data.get('max_requests')
    
    # Validar formato de month_year (YYYY-MM)
    try:
        datetime.strptime(month_year, '%Y-%m')
    except ValueError:
        return JsonResponse({'error': 'month_year debe tener formato YYYY-MM'}, status=400)
    
    # Validar max_requests
    try:
        max_requests = int(max_requests)
        if max_requests < 1:
            return JsonResponse({'error': 'max_requests debe ser al menos 1'}, status=400)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'max_requests debe ser un número entero'}, status=400)
    
    # Verificar que el usuario existe
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'usuario no encontrado'}, status=404)
    
    # Verificar si ya existe una cuota para ese usuario y mes
    if UserQuota.objects.filter(user_id=user_id, month_year=month_year).exists():
        return JsonResponse({
            'error': 'ya existe una cuota para este usuario y mes'
        }, status=409)
    
    # Crear cuota
    quota = UserQuota.objects.create(
        user_id=user_id,
        month_year=month_year,
        max_requests=max_requests,
        used_requests=0
    )
    
    quota_data = {
        'id': quota.id,
        'user_id': quota.user.id,
        'username': quota.user.username,
        'user_email': quota.user.email,
        'month_year': quota.month_year,
        'max_requests': quota.max_requests,
        'used_requests': quota.used_requests,
        'remaining_requests': quota.remaining_requests,
        'usage_percentage': quota.usage_percentage,
        'status': quota.status,
        'created_at': quota.created_at.isoformat(),
        'updated_at': quota.updated_at.isoformat(),
    }
    
    return JsonResponse({
        'quota': quota_data,
        'message': 'Cuota creada exitosamente'
    }, status=201)

@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
@admin_required
def admin_update_user_quota(request, quota_id):
    """Actualizar una cuota existente"""
    try:
        quota = UserQuota.objects.select_related('user').get(id=quota_id)
    except UserQuota.DoesNotExist:
        return JsonResponse({'error': 'cuota no encontrada'}, status=404)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Actualizar campos
    if 'max_requests' in data:
        try:
            max_requests = int(data['max_requests'])
            if max_requests < 1:
                return JsonResponse({'error': 'max_requests debe ser al menos 1'}, status=400)
            quota.max_requests = max_requests
        except (ValueError, TypeError):
            return JsonResponse({'error': 'max_requests debe ser un número entero'}, status=400)
    
    if 'used_requests' in data:
        try:
            used_requests = int(data['used_requests'])
            if used_requests < 0:
                return JsonResponse({'error': 'used_requests no puede ser negativo'}, status=400)
            quota.used_requests = used_requests
        except (ValueError, TypeError):
            return JsonResponse({'error': 'used_requests debe ser un número entero'}, status=400)
    
    quota.save()
    
    quota_data = {
        'id': quota.id,
        'user_id': quota.user.id,
        'username': quota.user.username,
        'user_email': quota.user.email,
        'month_year': quota.month_year,
        'max_requests': quota.max_requests,
        'used_requests': quota.used_requests,
        'remaining_requests': quota.remaining_requests,
        'usage_percentage': quota.usage_percentage,
        'status': quota.status,
        'created_at': quota.created_at.isoformat(),
        'updated_at': quota.updated_at.isoformat(),
    }
    
    return JsonResponse({
        'quota': quota_data,
        'message': 'Cuota actualizada exitosamente'
    })

@require_http_methods(["DELETE"])
@admin_required
def admin_delete_user_quota(request, quota_id):
    """Eliminar una cuota"""
    try:
        quota = UserQuota.objects.get(id=quota_id)
    except UserQuota.DoesNotExist:
        return JsonResponse({'error': 'cuota no encontrada'}, status=404)
    
    deleted_data = {
        'id': quota.id,
        'user_id': quota.user_id,
        'month_year': quota.month_year,
    }
    
    quota.delete()
    
    return JsonResponse({
        'message': 'Cuota eliminada exitosamente',
        'deleted': deleted_data
    })

@csrf_exempt
@require_http_methods(["POST"])
@admin_required
def admin_delete_quotas_bulk(request):
    """Eliminar múltiples cuotas"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    ids = data.get('ids', [])
    if not ids or not isinstance(ids, list) or len(ids) < 1:
        return JsonResponse({
            'error': 'Se requiere una lista de IDs con al menos un elemento'
        }, status=400)
    
    # Validar que todos los IDs sean enteros
    try:
        ids = [int(id_val) for id_val in ids]
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Los IDs deben ser números enteros'}, status=400)
    
    # Verificar que todas las cuotas existan
    existing_count = UserQuota.objects.filter(id__in=ids).count()
    if existing_count != len(ids):
        return JsonResponse({
            'error': 'una o más cuotas no existen',
            'found': existing_count,
            'requested': len(ids)
        }, status=404)
    
    # Eliminar en lote
    deleted_count, _ = UserQuota.objects.filter(id__in=ids).delete()
    
    return JsonResponse({
        'message': 'Cuotas eliminadas exitosamente',
        'deleted_count': deleted_count,
        'deleted_ids': ids
    })

@require_http_methods(["GET"])
@admin_required
def admin_export_quotas_csv(request):
    """Exportar cuotas a CSV"""
    import csv
    from django.http import HttpResponse
    
    # Obtener filtros (similares a admin_get_user_quotas)
    search = request.GET.get('search', '')
    month_year = request.GET.get('month_year')
    
    # Construir consulta
    query = UserQuota.objects.select_related('user')
    
    if search:
        query = query.filter(
            Q(user__username__icontains=search) |
            Q(user__email__icontains=search)
        )
    
    if month_year:
        query = query.filter(month_year=month_year)
    
    # Crear respuesta CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_quotas_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Usuario ID', 'Usuario', 'Email', 'Mes/Año', 
        'Máx. Solicitudes', 'Usadas', 'Restantes', 'Uso (%)', 'Estado',
        'Creada', 'Actualizada'
    ])
    
    for quota in query:
        writer.writerow([
            quota.id,
            quota.user.id,
            quota.user.username,
            quota.user.email,
            quota.month_year,
            quota.max_requests,
            quota.used_requests,
            quota.remaining_requests,
            quota.usage_percentage,
            quota.status,
            quota.created_at.isoformat(),
            quota.updated_at.isoformat(),
        ])
    
    return response




# ====== Vistas de Configuración del Sistema ======
@require_http_methods(["GET"])
@admin_required
def admin_get_system_configs(request):
    """Obtener todas las configuraciones del sistema"""
    try:
        configs = SystemConfig.objects.all()
        
        configs_data = []
        for config in configs:
            configs_data.append({
                'id': config.id,
                'key': config.key,
                'value': config.value,
                'description': config.description,
                'created_at': config.created_at.isoformat(),
                'updated_at': config.updated_at.isoformat(),
            })
        
        return JsonResponse(configs_data, safe=False)
    except Exception as e:
        logger.error(f"Error getting system configs: {str(e)}")
        return JsonResponse({'error': 'Error al obtener configuraciones'}, status=500)


@require_http_methods(["GET"])
@admin_required
def admin_get_system_config(request, config_id):
    """Obtener una configuración por ID"""
    try:
        config = SystemConfig.objects.get(id=config_id)
        
        config_data = {
            'id': config.id,
            'key': config.key,
            'value': config.value,
            'description': config.description,
            'created_at': config.created_at.isoformat(),
            'updated_at': config.updated_at.isoformat(),
        }
        
        return JsonResponse(config_data)
    except SystemConfig.DoesNotExist:
        return JsonResponse({'error': 'Configuración no encontrada'}, status=404)
    except Exception as e:
        logger.error(f"Error getting system config {config_id}: {str(e)}")
        return JsonResponse({'error': 'Error al obtener configuración'}, status=500)


@require_http_methods(["GET"])
@admin_required
def admin_get_system_config_by_key(request, key):
    """Obtener el valor de una configuración por su clave"""
    try:
        config = SystemConfig.objects.get(key=key)
        # Devolver solo el valor como texto plano
        return HttpResponse(config.value, content_type='text/plain')
    except SystemConfig.DoesNotExist:
        return JsonResponse({'error': 'Configuración no encontrada'}, status=404)
    except Exception as e:
        logger.error(f"Error getting system config by key {key}: {str(e)}")
        return JsonResponse({'error': 'Error al obtener configuración'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@admin_required
def admin_create_system_config(request):
    """Crear una nueva configuración"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Validar campos requeridos
    if 'key' not in data or not data['key']:
        return JsonResponse({'error': 'key es requerido'}, status=400)
    
    if 'value' not in data or data['value'] is None:
        return JsonResponse({'error': 'value es requerido'}, status=400)
    
    key = data['key'].strip()
    value = data['value']
    description = data.get('description', '').strip()
    
    # Verificar si la clave ya existe
    if SystemConfig.objects.filter(key=key).exists():
        return JsonResponse({'error': 'La clave ya existe'}, status=409)
    
    # Crear configuración
    try:
        config = SystemConfig.objects.create(
            key=key,
            value=value,
            description=description
        )
        
        config_data = {
            'id': config.id,
            'key': config.key,
            'value': config.value,
            'description': config.description,
            'created_at': config.created_at.isoformat(),
            'updated_at': config.updated_at.isoformat(),
        }
        
        return JsonResponse(config_data, status=201)
    except Exception as e:
        logger.error(f"Error creating system config: {str(e)}")
        return JsonResponse({'error': 'Error al crear configuración'}, status=500)

@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
@admin_required
def admin_update_system_config(request, config_id):
    """Actualizar una configuración existente"""
    try:
        config = SystemConfig.objects.get(id=config_id)
    except SystemConfig.DoesNotExist:
        return JsonResponse({'error': 'Configuración no encontrada'}, status=404)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Validar que al menos un campo para actualizar
    if not any(field in data for field in ['key', 'value', 'description']):
        return JsonResponse({'error': 'No hay campos para actualizar'}, status=400)
    
    # Preparar actualizaciones
    updates = {}
    
    if 'key' in data and data['key']:
        new_key = data['key'].strip()
        if new_key != config.key:
            # Verificar que la nueva clave no exista en otro registro
            if SystemConfig.objects.filter(key=new_key).exclude(id=config_id).exists():
                return JsonResponse({'error': 'La clave ya existe en otro registro'}, status=409)
            updates['key'] = new_key
    
    if 'value' in data and data['value'] is not None:
        updates['value'] = data['value']
    
    if 'description' in data:
        updates['description'] = data['description'].strip()
    
    # Aplicar actualizaciones
    try:
        for field, value in updates.items():
            setattr(config, field, value)
        config.save()
        
        config_data = {
            'id': config.id,
            'key': config.key,
            'value': config.value,
            'description': config.description,
            'created_at': config.created_at.isoformat(),
            'updated_at': config.updated_at.isoformat(),
        }
        
        return JsonResponse(config_data)
    except Exception as e:
        logger.error(f"Error updating system config {config_id}: {str(e)}")
        return JsonResponse({'error': 'Error al actualizar configuración'}, status=500)


@require_http_methods(["DELETE"])
@admin_required
@csrf_exempt
def admin_delete_system_config(request, config_id):
    """Eliminar una configuración"""
    try:
        config = SystemConfig.objects.get(id=config_id)
    except SystemConfig.DoesNotExist:
        return JsonResponse({'error': 'Configuración no encontrada'}, status=404)
    
    try:
        config_id_value = config.id
        config.delete()
        
        return JsonResponse({
            'message': 'Configuración eliminada correctamente',
            'id': config_id_value
        })
    except Exception as e:
        logger.error(f"Error deleting system config {config_id}: {str(e)}")
        return JsonResponse({'error': 'Error al eliminar configuración'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@admin_required
def admin_bulk_update_system_configs(request):
    """Actualizar múltiples configuraciones en lote"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Validar que data sea una lista
    if not isinstance(data, list):
        return JsonResponse({'error': 'Se esperaba una lista de configuraciones'}, status=400)
    
    if len(data) == 0:
        return JsonResponse({'error': 'La lista de configuraciones no puede estar vacía'}, status=400)
    
    # Validar cada item
    for i, item in enumerate(data):
        if 'key' not in item or not item['key']:
            return JsonResponse({'error': f'El item {i} no tiene key'}, status=400)
        if 'value' not in item or item['value'] is None:
            return JsonResponse({'error': f'El item {i} no tiene value'}, status=400)
    
    # Usar transacción atómica
    from django.db import transaction
    
    try:
        with transaction.atomic():
            updated_count = 0
            for item in data:
                key = item['key'].strip()
                value = item['value']
                
                # Buscar y actualizar
                updated = SystemConfig.objects.filter(key=key).update(value=value)
                if updated > 0:
                    updated_count += updated
                else:
                    # Opcional: crear si no existe
                    if item.get('create_if_not_exists', False):
                        SystemConfig.objects.create(
                            key=key,
                            value=value,
                            description=item.get('description', '')
                        )
                        updated_count += 1
        
        return JsonResponse({
            'message': f'Configuraciones actualizadas correctamente',
            'updated_count': updated_count
        })
    except Exception as e:
        logger.error(f"Error in bulk update system configs: {str(e)}")
        return JsonResponse({'error': 'Error al actualizar configuraciones'}, status=500)

@require_http_methods(["GET"])
@admin_required
def admin_export_system_configs_csv(request):
    """Exportar configuraciones a CSV"""
    import csv
    from django.http import HttpResponse
    
    # Obtener todas las configuraciones
    configs = SystemConfig.objects.all()
    
    # Crear respuesta CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="system_configs_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Clave', 'Valor', 'Descripción', 'Creada', 'Actualizada'
    ])
    
    for config in configs:
        writer.writerow([
            config.id,
            config.key,
            config.value,
            config.description,
            config.created_at.isoformat(),
            config.updated_at.isoformat(),
        ])
    
    return response

@require_http_methods(["GET"])
@admin_required
def admin_get_system_configs_grouped(request):
    """Obtener configuraciones agrupadas por prefijo de clave"""
    configs = SystemConfig.objects.all()
    
    grouped = {}
    for config in configs:
        # Obtener el prefijo (primera parte antes del punto)
        prefix = config.key.split('.')[0] if '.' in config.key else 'general'
        
        if prefix not in grouped:
            grouped[prefix] = []
        
        grouped[prefix].append({
            'id': config.id,
            'key': config.key,
            'value': config.value,
            'description': config.description,
        })
    
    return JsonResponse(grouped)

@require_http_methods(["GET"])
@admin_required
def admin_get_system_configs_by_prefix(request, prefix):
    """Obtener configuraciones por prefijo de clave"""
    try:
        configs = SystemConfig.objects.filter(key__startswith=f"{prefix}.")
        
        configs_data = []
        for config in configs:
            configs_data.append({
                'id': config.id,
                'key': config.key,
                'value': config.value,
                'description': config.description,
                'created_at': config.created_at.isoformat(),
                'updated_at': config.updated_at.isoformat(),
            })
        
        return JsonResponse(configs_data, safe=False)
    except Exception as e:
        logger.error(f"Error getting system configs by prefix {prefix}: {str(e)}")
        return JsonResponse({'error': 'Error al obtener configuraciones'}, status=500)
    



# ====== Estructuras para el dashboard ======

@require_http_methods(["GET"])
@admin_required
def admin_dashboard(request):
    """Endpoint principal del dashboard de administración"""
    
    # Obtener parámetros de filtro
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    limit = int(request.GET.get('limit', 10))
    
    # Validar límite
    if limit < 1 or limit > 50:
        limit = 10
    
    # Preparar respuesta
    dashboard = {
        'totals': {},
        'top_tests': {},
        'user_lists': {}
    }
    
    # Obtener todos los totales
    dashboard['totals'] = get_dashboard_totals(start_date, end_date)
    
    # Obtener listas de tests
    dashboard['top_tests'] = get_top_tests_lists(start_date, end_date, limit)
    
    # Obtener listas de usuarios
    dashboard['user_lists'] = get_user_lists(start_date, end_date, limit)
    
    return JsonResponse(dashboard)

def get_dashboard_totals(start_date=None, end_date=None):
    """Obtiene todos los totales del dashboard"""
    totals = {}
    
    # Construir filtros
    user_filters = Q()
    result_filters = Q()
    test_filters = Q()
    
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            user_filters &= Q(registered_at__date__gte=start)
            result_filters &= Q(started_at__date__gte=start)
            test_filters &= Q(created_at__date__gte=start)
        except ValueError:
            pass
    
    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            user_filters &= Q(registered_at__date__lte=end)
            result_filters &= Q(started_at__date__lte=end)
            test_filters &= Q(created_at__date__lte=end)
        except ValueError:
            pass
    
    # Total de usuarios registrados
    totals['total_users'] = User.objects.filter(user_filters).count()
    
    # Usuarios activos (con al menos 5 tests completados)
    active_users = User.objects.filter(
        user_filters,
        results__status='completed'
    ).annotate(
        test_count=Count('results')
    ).filter(test_count__gte=5).distinct().count()
    
    totals['active_users'] = active_users
    
    # Estadísticas de resultados
    completed_tests = Result.objects.filter(result_filters & Q(status='completed')).count()
    in_progress_tests = Result.objects.filter(result_filters & Q(status='in_progress')).count()
    expired_tests = Result.objects.filter(result_filters & Q(status='expired')).count()
    
    totals['completed_tests'] = completed_tests
    totals['in_progress_tests'] = in_progress_tests
    totals['expired_tests'] = expired_tests
    
    # Estadísticas de tests
    totals['total_tests'] = Test.objects.filter(test_filters).count()
    totals['inactive_tests'] = Test.objects.filter(test_filters & Q(is_active=False)).count()
    totals['advanced_tests'] = Test.objects.filter(test_filters & Q(level='Avanzado')).count()
    totals['intermediate_tests'] = Test.objects.filter(test_filters & Q(level='Intermedio')).count()
    totals['beginner_tests'] = Test.objects.filter(test_filters & Q(level='Principiante')).count()
    
    return totals

def get_top_tests_lists(start_date=None, end_date=None, limit=10):
    """Obtiene las listas de tests (top, peor rendimiento, etc.)"""
    
    top_tests = {}
    
    # Construir filtros para resultados
    result_filters = Q()
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            result_filters &= Q(results__started_at__date__gte=start)
        except ValueError:
            pass
    
    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            result_filters &= Q(results__started_at__date__lte=end)
        except ValueError:
            pass
    
    # 1. Tests más completados
    most_completed = Test.objects.annotate(
        completed_count=Count('results', filter=Q(results__status='completed') & result_filters)
    ).order_by('-completed_count')[:limit]
    
    top_tests['most_completed'] = [
        {'id': t.id, 'title': t.title, 'count': t.completed_count}
        for t in most_completed
    ]
    
    # 2. Tests más incompletos (en progreso)
    most_incomplete = Test.objects.annotate(
        in_progress_count=Count('results', filter=Q(results__status='in_progress') & result_filters)
    ).order_by('-in_progress_count')[:limit]
    
    top_tests['most_incomplete'] = [
        {'id': t.id, 'title': t.title, 'count': t.in_progress_count}
        for t in most_incomplete
    ]
    
    # 3. Tests más expirados
    most_expired = Test.objects.annotate(
        expired_count=Count('results', filter=Q(results__status='expired') & result_filters)
    ).order_by('-expired_count')[:limit]
    
    top_tests['most_expired'] = [
        {'id': t.id, 'title': t.title, 'count': t.expired_count}
        for t in most_expired
    ]
    
    # 4. Tests menos iniciados y más antiguos
    least_started_oldest = Test.objects.annotate(
        attempt_count=Count('results', filter=result_filters)
    ).order_by('attempt_count', 'created_at')[:limit]
    
    top_tests['least_started_oldest'] = [
        {
            'id': t.id, 
            'title': t.title, 
            'attempt_count': t.attempt_count,
            'date': t.created_at.isoformat()
        }
        for t in least_started_oldest
    ]
    
    # 5. Tests con mayor tasa de aciertos (usando consulta directa)
    # Crear subconsulta para resultados completados con filtros de fecha
    completed_results = Result.objects.filter(status='completed')
    
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            completed_results = completed_results.filter(started_at__date__gte=start)
        except ValueError:
            pass
    
    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            completed_results = completed_results.filter(started_at__date__lte=end)
        except ValueError:
            pass
    
    # Calcular accuracy por test
    accuracy_data = []
    tests_with_results = completed_results.values('test_id').distinct()
    
    for test_item in tests_with_results:
        test_id = test_item['test_id']
        test = Test.objects.get(id=test_id)
        
        results_for_test = completed_results.filter(test_id=test_id)
        total_correct = results_for_test.aggregate(total=Sum('correct_answers'))['total'] or 0
        total_wrong = results_for_test.aggregate(total=Sum('wrong_answers'))['total'] or 0
        total_attempts = results_for_test.count()
        
        total_questions = total_correct + total_wrong
        accuracy_rate = 0
        if total_questions > 0:
            accuracy_rate = (total_correct / total_questions) * 100
        
        accuracy_data.append({
            'id': test.id,
            'title': test.title,
            'accuracy_rate': round(accuracy_rate, 2),
            'total_attempts': total_attempts
        })
    
    # Ordenar por accuracy descendente
    accuracy_data.sort(key=lambda x: x['accuracy_rate'], reverse=True)
    top_tests['highest_accuracy'] = accuracy_data[:limit]
    
    # Ordenar por accuracy ascendente
    accuracy_data.sort(key=lambda x: x['accuracy_rate'])
    top_tests['lowest_accuracy'] = accuracy_data[:limit]
    
    # 6. Tests con mayor/menor tiempo promedio
    time_data = []
    for test_item in tests_with_results:
        test_id = test_item['test_id']
        test = Test.objects.get(id=test_id)
        
        results_for_test = completed_results.filter(test_id=test_id)
        avg_time = results_for_test.aggregate(avg=Avg('time_taken'))['avg'] or 0
        total_attempts = results_for_test.count()
        
        time_data.append({
            'id': test.id,
            'title': test.title,
            'avg_time': round(float(avg_time), 2),
            'total_attempts': total_attempts
        })
    
    # Mayor tiempo promedio
    time_data.sort(key=lambda x: x['avg_time'], reverse=True)
    top_tests['highest_avg_time'] = time_data[:limit]
    
    # Menor tiempo promedio
    time_data.sort(key=lambda x: x['avg_time'])
    top_tests['lowest_avg_time'] = time_data[:limit]
    
    return top_tests

def get_user_lists(start_date=None, end_date=None, limit=10):
    """Obtiene las listas de usuarios"""
    
    user_lists = {}
    
    # Construir filtros para usuarios
    user_filters = Q()
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            user_filters &= Q(registered_at__date__gte=start)
        except ValueError:
            pass
    
    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            user_filters &= Q(registered_at__date__lte=end)
        except ValueError:
            pass
    
    # 1. Nuevos usuarios por período
    new_users = User.objects.filter(user_filters).order_by('-registered_at')[:limit]
    
    user_lists['new_users_by_month'] = [
        {
            'id': u.id,
            'username': u.username,
            'role': u.role,
            'count': 1
        }
        for u in new_users
    ]
    
    # 2. Usuarios más activos (más tests completados)
    most_active = User.objects.annotate(
        completed_count=Count('results', filter=Q(results__status='completed'))
    ).filter(completed_count__gt=0).order_by('-completed_count')[:limit]
    
    user_lists['most_active_users'] = [
        {
            'id': u.id,
            'username': u.username,
            'role': u.role,
            'count': u.completed_count
        }
        for u in most_active
    ]
    
    # 3. Usuarios menos activos y más antiguos (sin tests completados)
    least_active_oldest = User.objects.annotate(
        completed_count=Count('results', filter=Q(results__status='completed'))
    ).filter(completed_count=0).order_by('registered_at')[:limit]
    
    user_lists['least_active_oldest'] = [
        {
            'id': u.id,
            'username': u.username,
            'role': u.role,
            'date': u.registered_at.isoformat()
        }
        for u in least_active_oldest
    ]
    
    # 4. Usuarios con login más reciente
    recent_login = User.objects.filter(
        login_at__isnull=False
    ).order_by('-login_at')[:limit]
    
    user_lists['recent_login'] = [
        {
            'id': u.id,
            'username': u.username,
            'role': u.role,
            'date': u.login_at.isoformat()
        }
        for u in recent_login
    ]
    
    # 5. Usuarios con login más antiguo
    oldest_login = User.objects.filter(
        login_at__isnull=False
    ).order_by('login_at')[:limit]
    
    user_lists['oldest_login'] = [
        {
            'id': u.id,
            'username': u.username,
            'role': u.role,
            'date': u.login_at.isoformat()
        }
        for u in oldest_login
    ]
    
    return user_lists

@require_http_methods(["GET"])
@admin_required
def get_test_detailed_stats(request, test_id):
    """Obtener estadísticas detalladas de un test específico"""
    
    try:
        test = Test.objects.prefetch_related('questions').get(id=test_id)
    except Test.DoesNotExist:
        return JsonResponse({'error': 'Test no encontrado'}, status=404)
    
    # Obtener estadísticas de resultados
    completed_results = Result.objects.filter(test_id=test_id, status='completed')
    all_results = Result.objects.filter(test_id=test_id)
    
    total_attempts = all_results.count()
    completed_attempts = completed_results.count()
    in_progress_attempts = all_results.filter(status='in_progress').count()
    expired_attempts = all_results.filter(status='expired').count()
    
    # Calcular promedios para tests completados
    avg_correct = completed_results.aggregate(avg=Avg('correct_answers'))['avg'] or 0
    avg_wrong = completed_results.aggregate(avg=Avg('wrong_answers'))['avg'] or 0
    avg_time = completed_results.aggregate(avg=Avg('time_taken'))['avg'] or 0
    
    # Calcular tasa de aciertos
    avg_accuracy = 0
    total_avg = avg_correct + avg_wrong
    if total_avg > 0:
        avg_accuracy = (avg_correct / total_avg) * 100
    
    # Calcular tasa de finalización
    completion_rate = 0
    if total_attempts > 0:
        completion_rate = (completed_attempts / total_attempts) * 100
    
    stats = {
        'test_title': test.title,
        'difficulty_level': test.level,
        'topic_hierarchy': {
            'main_topic': test.main_topic,
            'sub_topic': test.sub_topic,
            'specific_topic': test.specific_topic,
        },
        'total_attempts': total_attempts,
        'completed_attempts': completed_attempts,
        'in_progress_attempts': in_progress_attempts,
        'expired_attempts': expired_attempts,
        'avg_accuracy': round(avg_accuracy, 2),
        'avg_time': round(avg_time, 2),
        'completion_rate': round(completion_rate, 2),
    }
    
    return JsonResponse(stats)

@require_http_methods(["GET"])
@admin_required
def get_user_detailed_stats(request, user_id):
    """Obtener estadísticas detalladas de un usuario específico"""
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
    
    # Información del usuario
    user_info = {
        'username': user.username,
        'email': user.email,
        'registered_at': user.registered_at.isoformat() if user.registered_at else None,
        'last_login': user.login_at.isoformat() if user.login_at else None,
        'role': user.role,
    }
    
    # Estadísticas de tests
    user_results = Result.objects.filter(user_id=user_id)
    completed_results = user_results.filter(status='completed')
    
    total_tests = user_results.count()
    completed_tests = completed_results.count()
    in_progress_tests = user_results.filter(status='in_progress').count()
    expired_tests = user_results.filter(status='expired').count()
    
    # Calcular promedios
    avg_correct = completed_results.aggregate(avg=Avg('correct_answers'))['avg'] or 0
    avg_wrong = completed_results.aggregate(avg=Avg('wrong_answers'))['avg'] or 0
    avg_time = completed_results.aggregate(avg=Avg('time_taken'))['avg'] or 0
    
    # Calcular precisión promedio
    avg_accuracy = 0
    total_avg = avg_correct + avg_wrong
    if total_avg > 0:
        avg_accuracy = (avg_correct / total_avg) * 100
    
    # Obtener tema favorito
    favorite_topic = completed_results.values('test__main_topic').annotate(
        count=Count('id')
    ).order_by('-count').first()
    
    # Obtener nivel favorito
    favorite_level = completed_results.values('test__level').annotate(
        count=Count('id')
    ).order_by('-count').first()
    
    test_stats = {
        'total_tests': total_tests,
        'completed_tests': completed_tests,
        'in_progress_tests': in_progress_tests,
        'expired_tests': expired_tests,
        'avg_accuracy': round(avg_accuracy, 2),
        'avg_time_per_test': round(avg_time, 2),
        'favorite_topic': favorite_topic['test__main_topic'] if favorite_topic else 'N/A',
        'favorite_level': favorite_level['test__level'] if favorite_level else 'N/A',
    }
    
    # Actividad reciente (últimos 10 tests)
    recent_activity = user_results.select_related('test').order_by('-started_at')[:10]
    
    recent_activity_list = []
    for result in recent_activity:
        total_answers = result.correct_answers + result.wrong_answers
        accuracy = 0
        if total_answers > 0 and result.status == 'completed':
            accuracy = (result.correct_answers / total_answers) * 100
        
        recent_activity_list.append({
            'test_title': result.test.title,
            'status': result.status,
            'accuracy': round(accuracy, 2),
            'time_taken': result.time_taken,
            'started_at': result.started_at.isoformat(),
        })
    
    stats = {
        'user_info': user_info,
        'test_stats': test_stats,
        'recent_activity': recent_activity_list,
    }
    
    return JsonResponse(stats)

@require_http_methods(["GET"])
@admin_required
def get_dashboard_activity_summary(request):
    """Obtener resumen de actividad para el dashboard (gráficos)"""
    
    # Actividad de los últimos 30 días
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Resultados por día
    daily_results = []
    current_date = start_date
    while current_date <= end_date:
        daily_results.append({
            'date': current_date.isoformat(),
            'total': Result.objects.filter(started_at__date=current_date).count(),
            'completed': Result.objects.filter(started_at__date=current_date, status='completed').count(),
            'in_progress': Result.objects.filter(started_at__date=current_date, status='in_progress').count(),
            'expired': Result.objects.filter(started_at__date=current_date, status='expired').count(),
        })
        current_date += timedelta(days=1)
    
    # Nuevos usuarios por día
    daily_users = []
    current_date = start_date
    while current_date <= end_date:
        daily_users.append({
            'date': current_date.isoformat(),
            'count': User.objects.filter(registered_at__date=current_date).count(),
        })
        current_date += timedelta(days=1)
    
    # Tests creados por día
    daily_tests = []
    current_date = start_date
    while current_date <= end_date:
        daily_tests.append({
            'date': current_date.isoformat(),
            'count': Test.objects.filter(created_at__date=current_date).count(),
        })
        current_date += timedelta(days=1)
    
    return JsonResponse({
        'daily_results': daily_results,
        'daily_users': daily_users,
        'daily_tests': daily_tests,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
    })

@require_http_methods(["GET"])
@admin_required
def get_dashboard_performance_metrics(request):
    """Obtener métricas de rendimiento para el dashboard"""
    
    # Tasa de finalización general
    total_results = Result.objects.count()
    completed_results = Result.objects.filter(status='completed').count()
    completion_rate = (completed_results / total_results * 100) if total_results > 0 else 0
    
    # Precisión general
    completed_results_data = Result.objects.filter(status='completed').aggregate(
        total_correct=Sum('correct_answers'),
        total_answers=Sum(F('correct_answers') + F('wrong_answers'))
    )
    
    overall_accuracy = 0
    if completed_results_data['total_answers'] and completed_results_data['total_answers'] > 0:
        overall_accuracy = (completed_results_data['total_correct'] / completed_results_data['total_answers']) * 100
    
    # Tiempo promedio por test completado
    avg_time = Result.objects.filter(status='completed').aggregate(
        avg_time=Avg('time_taken')
    )['avg_time'] or 0
    
    # Distribución de niveles de tests
    level_distribution = list(Test.objects.values('level').annotate(
        count=Count('id')
    ))
    
    # Distribución de roles de usuarios
    role_distribution = list(User.objects.values('role').annotate(
        count=Count('id')
    ))
    
    return JsonResponse({
        'completion_rate': round(completion_rate, 2),
        'overall_accuracy': round(overall_accuracy, 2),
        'average_time_minutes': round(avg_time / 60, 2) if avg_time > 0 else 0,
        'level_distribution': level_distribution,
        'role_distribution': role_distribution,
    })


    