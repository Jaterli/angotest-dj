# users/services.py
from django.db.models import Count, Sum, F
from django.contrib.auth import get_user_model
from apps.results.models import Result

User = get_user_model()

# Constante para número mínimo de tests para rankings
MIN_TESTS_FOR_RANKING = 3

class DataService:
    """Servicio para obtener datos estadísticos del usuario"""
    
    def get_personal_data(self, user_id):
        """Obtiene datos personales del usuario"""
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return {
                'username': '',
                'email': '',
                'total_tests': 0,
                'avg_score': 0,
                'total_questions': 0,
                'total_correct': 0,
                'total_time': 0
            }
        
        # Estadísticas de resultados
        results = Result.objects.filter(user_id=user_id, status='completed')
        
        stats = results.aggregate(
            total_tests=Count('id', distinct=True),
            total_correct=Sum('correct_answers'),
            total_questions=Sum(F('correct_answers') + F('wrong_answers')),
            total_time=Sum('time_taken')
        )
        
        total_tests = stats['total_tests'] or 0
        total_correct = stats['total_correct'] or 0
        total_questions = stats['total_questions'] or 0
        
        avg_score = 0
        if total_questions > 0:
            avg_score = (total_correct / total_questions) * 100
        
        return {
            'username': user.username,
            'email': user.email,
            'total_tests': total_tests,
            'avg_score': round(avg_score, 2),
            'total_questions': total_questions,
            'total_correct': total_correct,
            'total_time': stats['total_time'] or 0
        }
    
    def get_personal_level_data(self, user_id):
        """Obtiene estadísticas por nivel para el usuario"""
        levels = ['Principiante', 'Intermedio', 'Avanzado']
        level_data = {}
        
        for level in levels:
            # Resultados de tests de este nivel
            results = Result.objects.filter(
                user_id=user_id,
                status='completed',
                test__level=level
            )
            
            stats = results.aggregate(
                total_tests=Count('id', distinct=True),
                total_correct=Sum('correct_answers'),
                total_questions=Sum(F('correct_answers') + F('wrong_answers')),
                total_time=Sum('time_taken')
            )
            
            total_tests = stats['total_tests'] or 0
            total_correct = stats['total_correct'] or 0
            total_questions = stats['total_questions'] or 0
            
            avg_score = 0
            if total_questions > 0:
                avg_score = (total_correct / total_questions) * 100
            
            level_data[level] = {
                'total_tests': total_tests,
                'avg_score': round(avg_score, 2),
                'total_questions': total_questions,
                'total_correct': total_correct,
                'total_time': stats['total_time'] or 0
            }
        
        return level_data
    
    def get_active_users_count(self):
        """Obtiene el número de usuarios activos (con al menos 1 test completado)"""
        return User.objects.filter(results__status='completed').distinct().count()
    
    def get_user_all_ranking_positions(self, user_id):
        """Obtiene todas las posiciones del usuario en los rankings"""
        from django.db import connection
        
        positions = {
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
        }
        
        # Posición por número de tests
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT rank FROM (
                    SELECT 
                        u.id,
                        ROW_NUMBER() OVER (ORDER BY COUNT(DISTINCT r.test_id) DESC) as rank
                    FROM users u
                    LEFT JOIN results r ON u.id = r.user_id AND r.status = 'completed'
                    GROUP BY u.id
                    HAVING COUNT(DISTINCT r.test_id) >= %s
                ) ranked
                WHERE id = %s
            """, [MIN_TESTS_FOR_RANKING, user_id])
            
            row = cursor.fetchone()
            if row:
                positions['by_tests'] = row[0]
        
        # Posición por precisión (todos los intentos)
        with connection.cursor() as cursor:
            cursor.execute("""
                WITH user_stats AS (
                    SELECT 
                        user_id,
                        SUM(correct_answers) as total_correct,
                        SUM(correct_answers + wrong_answers) as total_questions
                    FROM results
                    WHERE status = 'completed'
                    GROUP BY user_id
                    HAVING SUM(correct_answers + wrong_answers) > 0 
                        AND COUNT(DISTINCT test_id) >= %s
                )
                SELECT rank FROM (
                    SELECT 
                        user_id,
                        ROW_NUMBER() OVER (
                            ORDER BY (total_correct * 100.0 / total_questions) DESC
                        ) as rank
                    FROM user_stats
                ) ranked
                WHERE user_id = %s
            """, [MIN_TESTS_FOR_RANKING, user_id])
            
            row = cursor.fetchone()
            if row:
                positions['by_accuracy']['all_attempts'] = row[0]
        
        # Posición por tiempo promedio (todos los intentos)
        with connection.cursor() as cursor:
            cursor.execute("""
                WITH user_stats AS (
                    SELECT 
                        user_id,
                        SUM(time_taken) as total_time,
                        SUM(correct_answers + wrong_answers) as total_questions
                    FROM results
                    WHERE status = 'completed'
                    GROUP BY user_id
                    HAVING SUM(correct_answers + wrong_answers) > 0 
                        AND COUNT(DISTINCT test_id) >= %s
                )
                SELECT rank FROM (
                    SELECT 
                        user_id,
                        ROW_NUMBER() OVER (
                            ORDER BY (total_time * 1.0 / total_questions) ASC
                        ) as rank
                    FROM user_stats
                ) ranked
                WHERE user_id = %s
            """, [MIN_TESTS_FOR_RANKING, user_id])
            
            row = cursor.fetchone()
            if row:
                positions['by_avg_time']['all_attempts'] = row[0]
        
        # Posición por preguntas respondidas (todos los intentos)
        with connection.cursor() as cursor:
            cursor.execute("""
                WITH user_stats AS (
                    SELECT 
                        user_id,
                        SUM(correct_answers + wrong_answers) as total_questions
                    FROM results
                    WHERE status = 'completed'
                    GROUP BY user_id
                    HAVING SUM(correct_answers + wrong_answers) > 0 
                        AND COUNT(DISTINCT test_id) >= %s
                )
                SELECT rank FROM (
                    SELECT 
                        user_id,
                        ROW_NUMBER() OVER (ORDER BY total_questions DESC) as rank
                    FROM user_stats
                ) ranked
                WHERE user_id = %s
            """, [MIN_TESTS_FOR_RANKING, user_id])
            
            row = cursor.fetchone()
            if row:
                positions['by_questions']['all_attempts'] = row[0]
        
        # Posiciones por nivel
        levels = ['Principiante', 'Intermedio', 'Avanzado']
        for level in levels:
            # Por número de tests por nivel
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT rank FROM (
                        SELECT 
                            u.id,
                            ROW_NUMBER() OVER (ORDER BY COUNT(DISTINCT r.test_id) DESC) as rank
                        FROM users u
                        LEFT JOIN results r ON u.id = r.user_id AND r.status = 'completed'
                        LEFT JOIN tests t ON r.test_id = t.id AND t.level = %s
                        WHERE t.level IS NOT NULL
                        GROUP BY u.id
                        HAVING COUNT(DISTINCT r.test_id) >= %s
                    ) ranked
                    WHERE id = %s
                """, [level, MIN_TESTS_FOR_RANKING, user_id])
                
                row = cursor.fetchone()
                rank_by_tests = row[0] if row else 0
            
            # Por precisión por nivel
            with connection.cursor() as cursor:
                cursor.execute("""
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
                    SELECT rank FROM (
                        SELECT 
                            fa.user_id,
                            ROW_NUMBER() OVER (
                                ORDER BY (SUM(fa.correct_answers) * 100.0 / SUM(fa.correct_answers + fa.wrong_answers)) DESC
                            ) as rank
                        FROM first_attempt fa
                        JOIN tests t ON fa.test_id = t.id
                        WHERE t.level = %s AND fa.attempt_num = 1
                        GROUP BY fa.user_id
                        HAVING SUM(fa.correct_answers + fa.wrong_answers) > 0 
                            AND COUNT(DISTINCT fa.test_id) >= %s
                    ) ranked
                    WHERE user_id = %s
                """, [level, MIN_TESTS_FOR_RANKING, user_id])
                
                row = cursor.fetchone()
                rank_by_accuracy = row[0] if row else 0
            
            positions['levels'][level] = {
                'by_tests': rank_by_tests,
                'by_accuracy': rank_by_accuracy
            }
        
        return positions
    
    def get_community_averages(self):
        """Obtiene promedios de la comunidad"""
        from django.db import connection
        
        averages = {
            'overall': {
                'accuracy': 0,
                'avg_time_per_question': 0,
                'tests_per_user': 0
            },
            'levels': {}
        }
        
        # Promedio general de precisión
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    AVG(CASE 
                        WHEN total_questions > 0 
                        THEN (total_correct * 100.0 / total_questions)
                        ELSE 0 
                    END) as avg_accuracy
                FROM (
                    SELECT 
                        user_id,
                        SUM(correct_answers) as total_correct,
                        SUM(correct_answers + wrong_answers) as total_questions
                    FROM results
                    WHERE status = 'completed'
                    GROUP BY user_id
                    HAVING SUM(correct_answers + wrong_answers) > 0
                        AND COUNT(DISTINCT test_id) >= %s
                ) user_stats
            """, [MIN_TESTS_FOR_RANKING])
            
            row = cursor.fetchone()
            if row and row[0]:
                averages['overall']['accuracy'] = round(row[0], 2)
        
        # Tiempo promedio por pregunta
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT AVG(avg_time) FROM (
                    SELECT 
                        user_id,
                        AVG(time_taken * 1.0 / (correct_answers + wrong_answers)) as avg_time
                    FROM results
                    WHERE status = 'completed' AND (correct_answers + wrong_answers) > 0
                    GROUP BY user_id
                    HAVING COUNT(DISTINCT test_id) >= %s
                ) user_stats
            """, [MIN_TESTS_FOR_RANKING])
            
            row = cursor.fetchone()
            if row and row[0]:
                averages['overall']['avg_time_per_question'] = round(row[0], 2)
        
        # Tests por usuario
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT AVG(test_count) FROM (
                    SELECT 
                        user_id,
                        COUNT(DISTINCT test_id) as test_count
                    FROM results
                    WHERE status = 'completed'
                    GROUP BY user_id
                    HAVING COUNT(DISTINCT test_id) >= %s
                ) user_stats
            """, [MIN_TESTS_FOR_RANKING])
            
            row = cursor.fetchone()
            if row and row[0]:
                averages['overall']['tests_per_user'] = round(row[0], 2)
        
        # Promedios por nivel
        levels = ['Principiante', 'Intermedio', 'Avanzado']
        for level in levels:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        AVG(CASE 
                            WHEN total_questions > 0 
                            THEN (total_correct * 100.0 / total_questions)
                            ELSE 0 
                        END) as avg_accuracy,
                        AVG(avg_time_per_question) as avg_time
                    FROM (
                        SELECT 
                            r.user_id,
                            SUM(r.correct_answers) as total_correct,
                            SUM(r.correct_answers + r.wrong_answers) as total_questions,
                            AVG(r.time_taken * 1.0 / (r.correct_answers + r.wrong_answers)) as avg_time_per_question
                        FROM results r
                        JOIN tests t ON r.test_id = t.id
                        WHERE r.status = 'completed' AND t.level = %s
                            AND (r.correct_answers + r.wrong_answers) > 0
                        GROUP BY r.user_id
                        HAVING COUNT(DISTINCT r.test_id) >= %s
                    ) user_stats
                """, [level, MIN_TESTS_FOR_RANKING])
                
                row = cursor.fetchone()
                averages['levels'][level] = {
                    'accuracy': round(row[0], 2) if row and row[0] else 0,
                    'avg_time_per_question': round(row[1], 2) if row and row[1] else 0
                }
        
        return averages