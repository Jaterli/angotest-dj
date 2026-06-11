# users/services.py
from django.db.models import Count, Sum, Min, Avg, Q, F, Value
from django.db.models.functions import Coalesce, Round
from django.contrib.auth import get_user_model
from apps.results.models import Result

User = get_user_model()

# Constantes
MIN_TESTS_FOR_RANKING = 5
PREDEFINED_LEVELS = ['Principiante', 'Intermedio', 'Avanzado']

# Tipos de métricas
METRIC_TESTS_COUNT = 'completed_tests'
METRIC_AVG_TIME = 'time'
METRIC_ACCURACY = 'accuracy'
METRIC_QUESTIONS_ANSWERED = 'questions_answered'


class DataService:
    """Servicio para obtener datos estadísticos del usuario y comunidad"""
    
    def get_personal_data(self, user_id):
        """Obtiene estadísticas personales del usuario"""
        
        # Subconsulta para first attempt timestamps
        first_attempt_timestamps = Result.objects.filter(
            user_id=user_id,
            status='completed'
        ).values('test_id').annotate(
            first_updated=Min('updated_at')
        )
        
        # Contar estados
        status_counts = Result.objects.filter(user_id=user_id).aggregate(
            total_completed_all_attempts=Count('id', filter=Q(status='completed')),
            total_in_progress=Count('id', filter=Q(status='in_progress')),
            total_expired=Count('id', filter=Q(status='expired'))
        )
        
        # Todos los intentos
        all_attempts = Result.objects.filter(
            user_id=user_id,
            status='completed'
        ).aggregate(
            all_attempts_tests_count=Count('test_id', distinct=True),
            all_attempts_correct=Coalesce(Sum('correct_answers'), Value(0)),
            all_attempts_wrong=Coalesce(Sum('wrong_answers'), Value(0)),
            all_attempts_time_taken=Coalesce(Sum('time_taken'), Value(0)),
            all_attempts_questions_answered=Coalesce(
                Sum(F('correct_answers') + F('wrong_answers')), Value(0)
            )
        )
        
        # Primer intento
        first_attempt_ids = first_attempt_timestamps.values_list('test_id', flat=True)
        first_attempt = Result.objects.filter(
            user_id=user_id,
            status='completed',
            test_id__in=first_attempt_ids
        ).aggregate(
            first_attempt_tests_count=Count('test_id', distinct=True),
            first_attempt_correct=Coalesce(Sum('correct_answers'), Value(0)),
            first_attempt_wrong=Coalesce(Sum('wrong_answers'), Value(0)),
            first_attempt_time_taken=Coalesce(Sum('time_taken'), Value(0)),
            first_attempt_questions_answered=Coalesce(
                Sum(F('correct_answers') + F('wrong_answers')), Value(0)
            )
        )
        
        return {
            'completed_tests': status_counts['total_completed_all_attempts'] or 0,
            'in_progress_tests': status_counts['total_in_progress'] or 0,
            'expired_tests': status_counts['total_expired'] or 0,
            'all_attempts': {
                'tests_count': all_attempts['all_attempts_tests_count'] or 0,
                'total_correct': all_attempts['all_attempts_correct'] or 0,
                'total_wrong': all_attempts['all_attempts_wrong'] or 0,
                'total_time_taken': all_attempts['all_attempts_time_taken'] or 0,
                'total_questions_answered': all_attempts['all_attempts_questions_answered'] or 0,
            },
            'first_attempt': {
                'tests_count': first_attempt['first_attempt_tests_count'] or 0,
                'total_correct': first_attempt['first_attempt_correct'] or 0,
                'total_wrong': first_attempt['first_attempt_wrong'] or 0,
                'total_time_taken': first_attempt['first_attempt_time_taken'] or 0,
                'total_questions_answered': first_attempt['first_attempt_questions_answered'] or 0,
            }
        }
    
    def get_personal_level_data(self, user_id):
        """Obtiene estadísticas por nivel del usuario"""
        
        level_data = {}
        
        for level in PREDEFINED_LEVELS:
            # Todos los intentos para este nivel
            all_attempts = Result.objects.filter(
                user_id=user_id,
                status='completed',
                test__level=level
            ).aggregate(
                tests_count=Count('test_id', distinct=True),
                questions_count=Coalesce(Sum(F('correct_answers') + F('wrong_answers')), Value(0)),
                total_correct=Coalesce(Sum('correct_answers'), Value(0)),
                total_wrong=Coalesce(Sum('wrong_answers'), Value(0)),
                total_time_taken=Coalesce(Sum('time_taken'), Value(0))
            )
            
            # Primer intento para este nivel
            first_attempt_subquery = Result.objects.filter(
                user_id=user_id,
                status='completed',
                test__level=level
            ).values('test_id').annotate(
                first_updated=Min('updated_at')
            )
            
            first_attempt_ids = first_attempt_subquery.values_list('test_id', flat=True)
            
            first_attempt = Result.objects.filter(
                user_id=user_id,
                status='completed',
                test__level=level,
                test_id__in=first_attempt_ids
            ).aggregate(
                tests_count=Count('test_id', distinct=True),
                questions_count=Coalesce(Sum(F('correct_answers') + F('wrong_answers')), Value(0)),
                total_correct=Coalesce(Sum('correct_answers'), Value(0)),
                total_wrong=Coalesce(Sum('wrong_answers'), Value(0)),
                total_time_taken=Coalesce(Sum('time_taken'), Value(0))
            )
            
            level_data[level] = {
                'first_attempt': {
                    'tests_count': first_attempt['tests_count'] or 0,
                    'questions_count': first_attempt['questions_count'] or 0,
                    'total_correct': first_attempt['total_correct'] or 0,
                    'total_wrong': first_attempt['total_wrong'] or 0,
                    'total_time_taken': first_attempt['total_time_taken'] or 0,
                },
                'all_attempts': {
                    'tests_count': all_attempts['tests_count'] or 0,
                    'questions_count': all_attempts['questions_count'] or 0,
                    'total_correct': all_attempts['total_correct'] or 0,
                    'total_wrong': all_attempts['total_wrong'] or 0,
                    'total_time_taken': all_attempts['total_time_taken'] or 0,
                }
            }
        
        return level_data
    
    def get_active_users_count(self):
        """Obtiene usuarios con al menos MIN_TESTS_FOR_RANKING tests diferentes completados"""
        count = Result.objects.filter(
            status='completed'
        ).values('user_id').annotate(
            test_count=Count('test_id', distinct=True)
        ).filter(test_count__gte=MIN_TESTS_FOR_RANKING).count()
        
        return count
    
    def get_top_by_metric(self, metric, limit=10, level=None, min_tests=MIN_TESTS_FOR_RANKING):
        """Obtiene top por métrica específica"""
        
        if metric == 'top_by_tests':
            return self._get_top_by_tests(limit, min_tests)
        elif metric == 'top_by_level':
            return self._get_top_by_level(level, limit, min_tests)
        elif metric == 'top_by_levels_accuracy':
            return self._get_top_by_levels_accuracy(level, limit, min_tests)
        return []
    
    def _get_top_by_tests(self, limit, min_tests):
        """Obtiene top por cantidad de tests completados"""
        results = Result.objects.filter(
            status='completed'
        ).values('user_id', 'user__username').annotate(
            value=Count('test_id', distinct=True)
        ).filter(value__gt=min_tests).order_by('-value')[:limit]
        
        items = []
        rank = 1
        for item in results:
            items.append({
                'user_id': item['user_id'],
                'username': item['user__username'],
                'value': item['value'],
                'rank': rank
            })
            rank += 1
        
        return items
    
    def _get_top_by_level(self, level, limit, min_tests):
        """Obtiene top por nivel"""
        results = Result.objects.filter(
            status='completed',
            test__level=level
        ).values('user_id', 'user__username').annotate(
            value=Count('test_id', distinct=True)
        ).filter(value__gt=min_tests).order_by('-value')[:limit]
        
        items = []
        rank = 1
        for item in results:
            items.append({
                'user_id': item['user_id'],
                'username': item['user__username'],
                'value': item['value'],
                'rank': rank
            })
            rank += 1
        
        return items
    
    def _get_top_by_levels_accuracy(self, level, limit, min_tests):
        """Obtiene top por precisión por nivel"""
        
        # Subconsulta para primer intento
        first_attempts = Result.objects.filter(
            status='completed',
            test__level=level
        ).values('user_id', 'test_id').annotate(
            first_updated=Min('updated_at')
        )
        
        first_attempt_ids = []
        for fa in first_attempts:
            result = Result.objects.filter(
                user_id=fa['user_id'],
                test_id=fa['test_id'],
                updated_at=fa['first_updated']
            ).first()
            if result:
                first_attempt_ids.append(result.id)
        
        results = Result.objects.filter(
            id__in=first_attempt_ids
        ).values('user_id', 'user__username').annotate(
            total_correct=Sum('correct_answers'),
            total_questions=Sum(F('correct_answers') + F('wrong_answers'))
        ).filter(
            total_questions__gt=0
        ).annotate(
            value=Round(F('total_correct') * 100.0 / F('total_questions'), 2)
        ).filter(value__gt=0).order_by('-value')[:limit]
        
        items = []
        rank = 1
        for item in results:
            items.append({
                'user_id': item['user_id'],
                'username': item['user__username'],
                'value': float(item['value']),
                'rank': rank
            })
            rank += 1
        
        return items
    
    def get_top_by_avg_time(self, attempt_type='all', limit=10):
        """Obtiene top por tiempo promedio por pregunta"""
        
        query = Result.objects.filter(status='completed')
        
        if attempt_type == 'first':
            # Filtrar solo primeros intentos
            first_attempts = Result.objects.filter(
                status='completed'
            ).values('user_id', 'test_id').annotate(
                first_updated=Min('updated_at')
            )
            first_attempt_ids = []
            for fa in first_attempts:
                result = Result.objects.filter(
                    user_id=fa['user_id'],
                    test_id=fa['test_id'],
                    updated_at=fa['first_updated']
                ).first()
                if result:
                    first_attempt_ids.append(result.id)
            query = query.filter(id__in=first_attempt_ids)
        
        results = query.values('user_id', 'user__username').annotate(
            total_time=Sum('time_taken'),
            total_questions=Sum(F('correct_answers') + F('wrong_answers'))
        ).filter(
            total_questions__gt=0
        ).annotate(
            value=Round(F('total_time') * 1.0 / F('total_questions'), 2)
        ).order_by('value')[:limit]
        
        items = []
        rank = 1
        for item in results:
            items.append({
                'user_id': item['user_id'],
                'username': item['user__username'],
                'value': float(item['value']),
                'rank': rank
            })
            rank += 1
        
        return items
    
    def get_top_by_accuracy(self, attempt_type='all', limit=10):
        """Obtiene top por precisión"""
        
        query = Result.objects.filter(status='completed')
        
        if attempt_type == 'first':
            first_attempts = Result.objects.filter(
                status='completed'
            ).values('user_id', 'test_id').annotate(
                first_updated=Min('updated_at')
            )
            first_attempt_ids = []
            for fa in first_attempts:
                result = Result.objects.filter(
                    user_id=fa['user_id'],
                    test_id=fa['test_id'],
                    updated_at=fa['first_updated']
                ).first()
                if result:
                    first_attempt_ids.append(result.id)
            query = query.filter(id__in=first_attempt_ids)
        
        results = query.values('user_id', 'user__username').annotate(
            total_correct=Sum('correct_answers'),
            total_questions=Sum(F('correct_answers') + F('wrong_answers'))
        ).filter(
            total_questions__gt=0
        ).annotate(
            value=Round(F('total_correct') * 100.0 / F('total_questions'), 2)
        ).order_by('-value')[:limit]
        
        items = []
        rank = 1
        for item in results:
            items.append({
                'user_id': item['user_id'],
                'username': item['user__username'],
                'value': float(item['value']),
                'rank': rank
            })
            rank += 1
        
        return items
    
    def get_top_by_questions_answered(self, attempt_type='all', limit=10):
        """Obtiene top por preguntas respondidas"""
        
        query = Result.objects.filter(status='completed')
        
        if attempt_type == 'first':
            first_attempts = Result.objects.filter(
                status='completed'
            ).values('user_id', 'test_id').annotate(
                first_updated=Min('updated_at')
            )
            first_attempt_ids = []
            for fa in first_attempts:
                result = Result.objects.filter(
                    user_id=fa['user_id'],
                    test_id=fa['test_id'],
                    updated_at=fa['first_updated']
                ).first()
                if result:
                    first_attempt_ids.append(result.id)
            query = query.filter(id__in=first_attempt_ids)
        
        results = query.values('user_id', 'user__username').annotate(
            value=Coalesce(Sum(F('correct_answers') + F('wrong_answers')), Value(0))
        ).filter(value__gt=0).order_by('-value')[:limit]
        
        items = []
        rank = 1
        for item in results:
            items.append({
                'user_id': item['user_id'],
                'username': item['user__username'],
                'value': item['value'],
                'rank': rank
            })
            rank += 1
        
        return items
    
    def get_community_averages(self):
        """Obtiene promedios de la comunidad"""
        
        # Usuarios con suficientes tests
        active_users = Result.objects.filter(
            status='completed'
        ).values('user_id').annotate(
            test_count=Count('test_id', distinct=True)
        ).filter(test_count__gte=MIN_TESTS_FOR_RANKING).values_list('user_id', flat=True)
        
        # Todos los intentos
        all_stats = Result.objects.filter(
            user_id__in=active_users,
            status='completed'
        ).aggregate(
            total_time=Sum('time_taken'),
            total_questions=Sum(F('correct_answers') + F('wrong_answers')),
            total_correct=Sum('correct_answers')
        )
        
        # Primeros intentos
        first_attempts = Result.objects.filter(
            status='completed',
            user_id__in=active_users
        ).values('user_id', 'test_id').annotate(
            first_updated=Min('updated_at')
        )
        
        first_attempt_ids = []
        for fa in first_attempts:
            result = Result.objects.filter(
                user_id=fa['user_id'],
                test_id=fa['test_id'],
                updated_at=fa['first_updated']
            ).first()
            if result:
                first_attempt_ids.append(result.id)
        
        first_stats = Result.objects.filter(
            id__in=first_attempt_ids
        ).aggregate(
            total_time=Sum('time_taken'),
            total_questions=Sum(F('correct_answers') + F('wrong_answers')),
            total_correct=Sum('correct_answers')
        )
        
        # Calcular promedios
        avg_time_all = 0
        if all_stats['total_questions'] and all_stats['total_questions'] > 0:
            avg_time_all = all_stats['total_time'] / all_stats['total_questions']
        
        avg_time_first = 0
        if first_stats['total_questions'] and first_stats['total_questions'] > 0:
            avg_time_first = first_stats['total_time'] / first_stats['total_questions']
        
        avg_accuracy_all = 0
        if all_stats['total_questions'] and all_stats['total_questions'] > 0:
            avg_accuracy_all = (all_stats['total_correct'] / all_stats['total_questions']) * 100
        
        avg_accuracy_first = 0
        if first_stats['total_questions'] and first_stats['total_questions'] > 0:
            avg_accuracy_first = (first_stats['total_correct'] / first_stats['total_questions']) * 100
        
        # Promedio de preguntas por usuario
        user_questions_all = Result.objects.filter(
            user_id__in=active_users,
            status='completed'
        ).values('user_id').annotate(
            total_questions=Sum(F('correct_answers') + F('wrong_answers'))
        ).aggregate(avg=Avg('total_questions'))
        
        user_questions_first = Result.objects.filter(
            id__in=first_attempt_ids
        ).values('user_id').annotate(
            total_questions=Sum(F('correct_answers') + F('wrong_answers'))
        ).aggregate(avg=Avg('total_questions'))
        
        # Obtener estadísticas por nivel
        level_stats = self.get_community_level_stats()
        
        return {
            'all_attempts': {
                'avg_time_taken_per_question': round(avg_time_all, 2),
                'avg_accuracy': round(avg_accuracy_all, 2),
                'avg_questions_per_user': round(user_questions_all['avg'] or 0, 2)
            },
            'first_attempt': {
                'avg_time_taken_per_question': round(avg_time_first, 2),
                'avg_accuracy': round(avg_accuracy_first, 2),
                'avg_questions_per_user': round(user_questions_first['avg'] or 0, 2)
            },
            'levels': level_stats
        }
    
    def get_community_level_stats(self):
        """Obtiene estadísticas de comunidad por nivel"""
        
        level_stats = {}
        
        for level in PREDEFINED_LEVELS:
            # Usuarios activos en este nivel
            active_users = Result.objects.filter(
                status='completed',
                test__level=level
            ).values('user_id').annotate(
                test_count=Count('test_id', distinct=True)
            ).filter(test_count__gte=1).values_list('user_id', flat=True)
            
            # Todos los intentos
            all_stats = Result.objects.filter(
                user_id__in=active_users,
                status='completed',
                test__level=level
            ).aggregate(
                total_time=Sum('time_taken'),
                total_questions=Sum(F('correct_answers') + F('wrong_answers')),
                total_correct=Sum('correct_answers')
            )
            
            # Primeros intentos
            first_attempts = Result.objects.filter(
                status='completed',
                test__level=level,
                user_id__in=active_users
            ).values('user_id', 'test_id').annotate(
                first_updated=Min('updated_at')
            )
            
            first_attempt_ids = []
            for fa in first_attempts:
                result = Result.objects.filter(
                    user_id=fa['user_id'],
                    test_id=fa['test_id'],
                    updated_at=fa['first_updated']
                ).first()
                if result:
                    first_attempt_ids.append(result.id)
            
            first_stats = Result.objects.filter(
                id__in=first_attempt_ids
            ).aggregate(
                total_time=Sum('time_taken'),
                total_questions=Sum(F('correct_answers') + F('wrong_answers')),
                total_correct=Sum('correct_answers')
            )
            
            # Calcular promedios
            avg_time_all = 0
            if all_stats['total_questions'] and all_stats['total_questions'] > 0:
                avg_time_all = all_stats['total_time'] / all_stats['total_questions']
            
            avg_time_first = 0
            if first_stats['total_questions'] and first_stats['total_questions'] > 0:
                avg_time_first = first_stats['total_time'] / first_stats['total_questions']
            
            avg_accuracy_all = 0
            if all_stats['total_questions'] and all_stats['total_questions'] > 0:
                avg_accuracy_all = (all_stats['total_correct'] / all_stats['total_questions']) * 100
            
            avg_accuracy_first = 0
            if first_stats['total_questions'] and first_stats['total_questions'] > 0:
                avg_accuracy_first = (first_stats['total_correct'] / first_stats['total_questions']) * 100
            
            # Promedio de preguntas por usuario
            user_questions_all = Result.objects.filter(
                user_id__in=active_users,
                status='completed',
                test__level=level
            ).values('user_id').annotate(
                total_questions=Sum(F('correct_answers') + F('wrong_answers'))
            ).aggregate(avg=Avg('total_questions'))
            
            user_questions_first = Result.objects.filter(
                id__in=first_attempt_ids
            ).values('user_id').annotate(
                total_questions=Sum(F('correct_answers') + F('wrong_answers'))
            ).aggregate(avg=Avg('total_questions'))
            
            level_stats[level] = {
                'all_attempts': {
                    'avg_time_taken_per_question': round(avg_time_all, 2),
                    'avg_accuracy': round(avg_accuracy_all, 2),
                    'avg_questions_per_user': round(user_questions_all['avg'] or 0, 2)
                },
                'first_attempt': {
                    'avg_time_taken_per_question': round(avg_time_first, 2),
                    'avg_accuracy': round(avg_accuracy_first, 2),
                    'avg_questions_per_user': round(user_questions_first['avg'] or 0, 2)
                }
            }
        
        return level_stats
    
    def get_ranking_position_by_metric(self, user_id, metric_type, attempt_type='all', level=None):
        """Obtiene la posición del usuario en una métrica específica"""
        
        if metric_type == METRIC_TESTS_COUNT:
            return self._get_position_tests_count(user_id)
        elif metric_type == METRIC_AVG_TIME:
            return self._get_position_avg_time(user_id, attempt_type)
        elif metric_type == METRIC_ACCURACY:
            return self._get_position_accuracy(user_id, attempt_type)
        elif metric_type == METRIC_QUESTIONS_ANSWERED:
            return self._get_position_questions_answered(user_id, attempt_type)
        elif metric_type == 'level_accuracy' and level:
            return self._get_position_level_accuracy(user_id, level)
        
        return 0
    
    def _get_position_tests_count(self, user_id):
        """Obtiene posición por cantidad de tests"""
        user_tests = Result.objects.filter(
            user_id=user_id,
            status='completed'
        ).values('test_id').distinct().count()
        
        if user_tests == 0:
            return 0
        
        higher_count = Result.objects.filter(
            status='completed'
        ).values('user_id').annotate(
            test_count=Count('test_id', distinct=True)
        ).filter(test_count__gt=user_tests).count()
        
        return higher_count + 1
    
    def _get_position_avg_time(self, user_id, attempt_type):
        """Obtiene posición por tiempo promedio"""
        
        query = Result.objects.filter(status='completed')
        
        if attempt_type == 'first':
            first_attempts = Result.objects.filter(
                status='completed'
            ).values('user_id', 'test_id').annotate(
                first_updated=Min('updated_at')
            )
            first_attempt_ids = []
            for fa in first_attempts:
                result = Result.objects.filter(
                    user_id=fa['user_id'],
                    test_id=fa['test_id'],
                    updated_at=fa['first_updated']
                ).first()
                if result:
                    first_attempt_ids.append(result.id)
            query = query.filter(id__in=first_attempt_ids)
        
        user_avg = query.filter(user_id=user_id).values('user_id').annotate(
            total_time=Sum('time_taken'),
            total_questions=Sum(F('correct_answers') + F('wrong_answers'))
        ).filter(total_questions__gt=0).annotate(
            avg_time=F('total_time') * 1.0 / F('total_questions')
        ).first()
        
        if not user_avg or user_avg['avg_time'] is None:
            return 0
        
        lower_count = query.values('user_id').annotate(
            total_time=Sum('time_taken'),
            total_questions=Sum(F('correct_answers') + F('wrong_answers'))
        ).filter(
            total_questions__gt=0
        ).annotate(
            avg_time=F('total_time') * 1.0 / F('total_questions')
        ).filter(
            avg_time__lt=user_avg['avg_time'],
            avg_time__isnull=False
        ).count()
        
        return lower_count + 1
    
    def _get_position_accuracy(self, user_id, attempt_type):
        """Obtiene posición por precisión"""
        
        query = Result.objects.filter(status='completed')
        
        if attempt_type == 'first':
            first_attempts = Result.objects.filter(
                status='completed'
            ).values('user_id', 'test_id').annotate(
                first_updated=Min('updated_at')
            )
            first_attempt_ids = []
            for fa in first_attempts:
                result = Result.objects.filter(
                    user_id=fa['user_id'],
                    test_id=fa['test_id'],
                    updated_at=fa['first_updated']
                ).first()
                if result:
                    first_attempt_ids.append(result.id)
            query = query.filter(id__in=first_attempt_ids)
        
        user_acc = query.filter(user_id=user_id).values('user_id').annotate(
            total_correct=Sum('correct_answers'),
            total_questions=Sum(F('correct_answers') + F('wrong_answers'))
        ).filter(total_questions__gt=0).annotate(
            accuracy=F('total_correct') * 100.0 / F('total_questions')
        ).first()
        
        if not user_acc or user_acc['accuracy'] is None:
            return 0
        
        higher_count = query.values('user_id').annotate(
            total_correct=Sum('correct_answers'),
            total_questions=Sum(F('correct_answers') + F('wrong_answers'))
        ).filter(
            total_questions__gt=0
        ).annotate(
            accuracy=F('total_correct') * 100.0 / F('total_questions')
        ).filter(
            accuracy__gt=user_acc['accuracy'],
            accuracy__isnull=False
        ).count()
        
        return higher_count + 1
    
    def _get_position_questions_answered(self, user_id, attempt_type):
        """Obtiene posición por preguntas respondidas"""
        
        query = Result.objects.filter(status='completed')
        
        if attempt_type == 'first':
            first_attempts = Result.objects.filter(
                status='completed'
            ).values('user_id', 'test_id').annotate(
                first_updated=Min('updated_at')
            )
            first_attempt_ids = []
            for fa in first_attempts:
                result = Result.objects.filter(
                    user_id=fa['user_id'],
                    test_id=fa['test_id'],
                    updated_at=fa['first_updated']
                ).first()
                if result:
                    first_attempt_ids.append(result.id)
            query = query.filter(id__in=first_attempt_ids)
        
        user_questions = query.filter(user_id=user_id).aggregate(
            total=Coalesce(Sum(F('correct_answers') + F('wrong_answers')), Value(0))
        )['total']
        
        if user_questions == 0:
            return 0
        
        higher_count = query.values('user_id').annotate(
            total=Coalesce(Sum(F('correct_answers') + F('wrong_answers')), Value(0))
        ).filter(total__gt=user_questions).count()
        
        return higher_count + 1
    
    def _get_position_level_accuracy(self, user_id, level):
        """Obtiene posición por precisión por nivel"""
        
        # Obtener precisión del usuario para este nivel (primer intento)
        first_attempts = Result.objects.filter(
            user_id=user_id,
            status='completed',
            test__level=level
        ).values('test_id').annotate(
            first_updated=Min('updated_at')
        )
        
        first_attempt_ids = []
        for fa in first_attempts:
            result = Result.objects.filter(
                user_id=user_id,
                test_id=fa['test_id'],
                updated_at=fa['first_updated']
            ).first()
            if result:
                first_attempt_ids.append(result.id)
        
        user_stats = Result.objects.filter(
            id__in=first_attempt_ids
        ).aggregate(
            total_correct=Sum('correct_answers'),
            total_questions=Sum(F('correct_answers') + F('wrong_answers'))
        )
        
        if not user_stats['total_questions'] or user_stats['total_questions'] == 0:
            return 0
        
        user_accuracy = (user_stats['total_correct'] / user_stats['total_questions']) * 100
        
        # Contar usuarios con mayor precisión
        all_users_first_attempts = Result.objects.filter(
            status='completed',
            test__level=level
        ).values('user_id', 'test_id').annotate(
            first_updated=Min('updated_at')
        )
        
        all_first_attempt_ids = []
        for fa in all_users_first_attempts:
            result = Result.objects.filter(
                user_id=fa['user_id'],
                test_id=fa['test_id'],
                updated_at=fa['first_updated']
            ).first()
            if result:
                all_first_attempt_ids.append(result.id)
        
        higher_count = Result.objects.filter(
            id__in=all_first_attempt_ids
        ).values('user_id').annotate(
            total_correct=Sum('correct_answers'),
            total_questions=Sum(F('correct_answers') + F('wrong_answers'))
        ).filter(
            total_questions__gt=0
        ).annotate(
            accuracy=F('total_correct') * 100.0 / F('total_questions')
        ).filter(
            accuracy__gt=user_accuracy
        ).count()
        
        return higher_count + 1
    
    def get_user_all_ranking_positions(self, user_id):
        """Obtiene todas las posiciones del usuario en una sola llamada"""
        
        positions = {
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
        }
        
        # Posición en tests completados
        positions['completed_tests'] = self._get_position_tests_count(user_id)
        
        # Posiciones para todos los intentos
        positions['all_attempts']['avg_time_taken_per_question'] = self._get_position_avg_time(user_id, 'all')
        positions['all_attempts']['accuracy'] = self._get_position_accuracy(user_id, 'all')
        positions['all_attempts']['questions_answered'] = self._get_position_questions_answered(user_id, 'all')
        
        # Posiciones para primeros intentos
        positions['first_attempt']['avg_time_taken_per_question'] = self._get_position_avg_time(user_id, 'first')
        positions['first_attempt']['accuracy'] = self._get_position_accuracy(user_id, 'first')
        positions['first_attempt']['questions_answered'] = self._get_position_questions_answered(user_id, 'first')
        
        # Posiciones por nivel
        for level in PREDEFINED_LEVELS:
            positions['levels'][level] = {
                'first_attempt': self._get_position_level_accuracy(user_id, level)
            }
        
        # Total de usuarios activos
        positions['total_active_users'] = self.get_active_users_count()
        
        return positions