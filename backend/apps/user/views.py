# users/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import connection
from .services import DataService, MIN_TESTS_FOR_RANKING
import logging

logger = logging.getLogger(__name__)

# ====== Dashboard Personal ======

@require_http_methods(["GET"])
def get_dashboard_data(request):
    """Obtiene datos del dashboard personal del usuario"""
    
    user_id = request.user.id
    
    data_service = DataService()
    
    # Obtener datos en paralelo (simulando goroutines con consultas secuenciales)
    personal_data = data_service.get_personal_data(user_id)
    level_data = data_service.get_personal_level_data(user_id)
    total_active_users = data_service.get_active_users_count()
    
    response = {
        'personal_data': personal_data,
        'level_data': level_data,
        'total_active_users': total_active_users
    }
    
    return JsonResponse(response)

# ====== Rankings ======

def get_top_by_metric(metric, args):
    """Función genérica para obtener tops"""
    from django.db import connection
    
    queries = {
        'top_by_tests': """
            SELECT 
                u.id as user_id,
                u.username,
                COALESCE(COUNT(DISTINCT r.test_id), 0) as value,
                ROW_NUMBER() OVER (ORDER BY COUNT(DISTINCT r.test_id) DESC) as rank
            FROM users u
            LEFT JOIN results r ON u.id = r.user_id AND r.status = 'completed'
            GROUP BY u.id, u.username
            HAVING COUNT(DISTINCT r.test_id) >= %s
            ORDER BY rank
            LIMIT %s
        """,
        
        'top_by_level': """
            SELECT 
                u.id as user_id,
                u.username,
                COALESCE(COUNT(DISTINCT r.test_id), 0) as value,
                ROW_NUMBER() OVER (ORDER BY COUNT(DISTINCT r.test_id) DESC) as rank
            FROM users u
            LEFT JOIN results r ON u.id = r.user_id AND r.status = 'completed'
            LEFT JOIN tests t ON r.test_id = t.id AND t.level = %s
            WHERE t.level IS NOT NULL
            GROUP BY u.id, u.username
            HAVING COUNT(DISTINCT r.test_id) >= %s
            ORDER BY rank
            LIMIT %s
        """,
        
        'top_by_levels_accuracy': """
            WITH first_attempt AS (
                SELECT
                    r.user_id,
                    r.test_id,
                    r.correct_answers,
                    r.wrong_answers,
                    ROW_NUMBER() OVER (
                        PARTITION BY r.user_id, r.test_id
                        ORDER BY r.updated_at ASC
                    ) AS attempt_num
                FROM results r
                WHERE r.status = 'completed'
            )
            SELECT 
                u.id AS user_id,
                u.username,
                CASE 
                    WHEN SUM(fa.correct_answers + fa.wrong_answers) > 0
                    THEN ROUND((SUM(fa.correct_answers) * 100.0) / SUM(fa.correct_answers + fa.wrong_answers), 2)
                    ELSE 0
                END AS value,
                ROW_NUMBER() OVER (
                    ORDER BY
                        CASE 
                            WHEN SUM(fa.correct_answers + fa.wrong_answers) > 0
                            THEN (SUM(fa.correct_answers) * 100.0) / SUM(fa.correct_answers + fa.wrong_answers)
                            ELSE 0
                        END DESC
                ) AS rank
            FROM users u
            JOIN first_attempt fa ON fa.user_id = u.id AND fa.attempt_num = 1
            JOIN tests t ON fa.test_id = t.id
            WHERE t.level = %s
            GROUP BY u.id, u.username
            HAVING SUM(fa.correct_answers + fa.wrong_answers) > 0 
                AND COUNT(DISTINCT fa.test_id) >= %s
            ORDER BY rank
            LIMIT %s
        """
    }
    
    query = queries.get(metric)
    if not query:
        return []
    
    with connection.cursor() as cursor:
        cursor.execute(query, args)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
    items = []
    for row in rows:
        items.append(dict(zip(columns, row)))
    
    return items


def get_top_by_avg_time(attempt_type, limit):
    """Obtiene top por tiempo promedio"""
    with connection.cursor() as cursor:
        query = """
            WITH user_stats AS (
                SELECT 
                    r.user_id,
                    SUM(r.time_taken) as total_time,
                    SUM(r.correct_answers + r.wrong_answers) as total_questions_answered,
                    COUNT(DISTINCT r.test_id) as tests_count
                FROM results r
                WHERE r.status = 'completed'
        """
        
        if attempt_type == "first":
            query += """
                AND (r.user_id, r.test_id, r.updated_at) IN (
                    SELECT 
                        user_id,
                        test_id,
                        MIN(updated_at) as first_updated
                    FROM results 
                    WHERE status = 'completed'
                    GROUP BY user_id, test_id
                )
            """
        
        query += """
                GROUP BY r.user_id
                HAVING SUM(r.correct_answers + r.wrong_answers) > 0 
                    AND COUNT(DISTINCT r.test_id) >= %s
            )
            SELECT 
                u.id as user_id,
                u.username,
                CASE 
                    WHEN us.total_questions_answered > 0 
                    THEN ROUND(us.total_time * 1.0 / us.total_questions_answered, 2)
                    ELSE 0 
                END as value,
                ROW_NUMBER() OVER (ORDER BY 
                    CASE 
                        WHEN us.total_questions_answered > 0 
                        THEN us.total_time * 1.0 / us.total_questions_answered
                        ELSE 0 
                    END ASC
                ) as rank
            FROM users u
            INNER JOIN user_stats us ON u.id = us.user_id
            ORDER BY rank
            LIMIT %s
        """
        
        cursor.execute(query, [MIN_TESTS_FOR_RANKING, limit])
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
    items = []
    for row in rows:
        items.append(dict(zip(columns, row)))
    
    return items


def get_top_by_accuracy(attempt_type, limit):
    """Obtiene top por precisión"""
    with connection.cursor() as cursor:
        query = """
            WITH user_stats AS (
                SELECT 
                    r.user_id,
                    SUM(r.correct_answers) as total_correct,
                    SUM(r.correct_answers + r.wrong_answers) as total_questions_answered,
                    COUNT(DISTINCT r.test_id) as tests_count
                FROM results r
                WHERE r.status = 'completed'
        """
        
        if attempt_type == "first":
            query += """
                AND (r.user_id, r.test_id, r.updated_at) IN (
                    SELECT 
                        user_id,
                        test_id,
                        MIN(updated_at) as first_updated
                    FROM results 
                        WHERE status = 'completed'
                    GROUP BY user_id, test_id
                )
            """
        
        query += """
                GROUP BY r.user_id
                HAVING SUM(r.correct_answers + r.wrong_answers) > 0 
                    AND COUNT(DISTINCT r.test_id) >= %s
            )
            SELECT 
                u.id as user_id,
                u.username,
                CASE 
                    WHEN us.total_questions_answered > 0 
                    THEN ROUND((us.total_correct * 100.0) / us.total_questions_answered, 2)
                    ELSE 0 
                END as value,
                ROW_NUMBER() OVER (ORDER BY 
                    CASE 
                        WHEN us.total_questions_answered > 0 
                        THEN (us.total_correct * 100.0) / us.total_questions_answered
                        ELSE 0 
                    END DESC
                ) as rank
            FROM users u
            INNER JOIN user_stats us ON u.id = us.user_id
            ORDER BY rank
            LIMIT %s
        """
        
        cursor.execute(query, [MIN_TESTS_FOR_RANKING, limit])
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
    items = []
    for row in rows:
        items.append(dict(zip(columns, row)))
    
    return items


def get_top_by_questions_answered(attempt_type, limit):
    """Obtiene top por preguntas respondidas"""
    with connection.cursor() as cursor:
        query = """
            WITH user_stats AS (
                SELECT 
                    r.user_id,
                    SUM(r.correct_answers + r.wrong_answers) as total_questions_answered,
                    COUNT(DISTINCT r.test_id) as tests_count
                FROM results r
                WHERE r.status = 'completed'
        """
        
        if attempt_type == "first":
            query += """
                AND (r.user_id, r.test_id, r.updated_at) IN (
                    SELECT 
                        user_id,
                        test_id,
                        MIN(updated_at) as first_updated
                    FROM results 
                    WHERE status = 'completed'
                    GROUP BY user_id, test_id
                )
            """
        
        query += """
                GROUP BY r.user_id
                HAVING SUM(r.correct_answers + r.wrong_answers) > 0 
                    AND COUNT(DISTINCT r.test_id) >= %s
            )
            SELECT 
                u.id as user_id,
                u.username,
                COALESCE(us.total_questions_answered, 0) as value,
                ROW_NUMBER() OVER (ORDER BY COALESCE(us.total_questions_answered, 0) DESC) as rank
            FROM users u
            INNER JOIN user_stats us ON u.id = us.user_id
            ORDER BY rank
            LIMIT %s
        """
        
        cursor.execute(query, [MIN_TESTS_FOR_RANKING, limit])
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
    items = []
    for row in rows:
        items.append(dict(zip(columns, row)))
    
    return items


@require_http_methods(["GET"])
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
            'by_tests': 0,
            'by_accuracy': {
                'all_attempts': 0,
                'first_attempt': 0
            },
            'by_avg_time': {
                'all_attempts': 0,
                'first_attempt': 0
            },
            'by_questions': {
                'all_attempts': 0,
                'first_attempt': 0
            },
            'levels': {}
        },
        'community_averages': {
            'overall': {
                'accuracy': 0,
                'avg_time_per_question': 0,
                'tests_per_user': 0
            },
            'levels': {}
        },
        'min_tests_for_ranking': MIN_TESTS_FOR_RANKING
    }
    
    # Obtener tops
    response['top_by_tests'] = get_top_by_metric('top_by_tests', [MIN_TESTS_FOR_RANKING, limit])
    
    response['top_by_avg_time_taken_per_question']['all_attempts'] = get_top_by_avg_time('all', limit)
    response['top_by_avg_time_taken_per_question']['first_attempt'] = get_top_by_avg_time('first', limit)
    
    response['top_by_accuracy']['all_attempts'] = get_top_by_accuracy('all', limit)
    response['top_by_accuracy']['first_attempt'] = get_top_by_accuracy('first', limit)
    
    response['top_by_questions_answered']['all_attempts'] = get_top_by_questions_answered('all', limit)
    response['top_by_questions_answered']['first_attempt'] = get_top_by_questions_answered('first', limit)
    
    # Rankings por niveles
    levels = ['Principiante', 'Intermedio', 'Avanzado']
    for level in levels:
        response['top_by_levels'][level] = get_top_by_metric('top_by_level', [level, MIN_TESTS_FOR_RANKING, limit])
        response['top_by_levels_accuracy'][level] = get_top_by_metric('top_by_levels_accuracy', [level, MIN_TESTS_FOR_RANKING, limit])
    
    # Obtener posición del usuario
    positions = data_service.get_user_all_ranking_positions(user_id)
    if positions:
        response['current_user_position'] = positions
    
    # Obtener promedios de comunidad
    averages = data_service.get_community_averages()
    if averages:
        response['community_averages'] = averages
    
    return JsonResponse(response)