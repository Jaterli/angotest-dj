from django.db.models import Count, Q, Sum, Avg, F, Value, FloatField, Window
from django.db.models.functions import Rank, Coalesce
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Test
from apps.results.models import Result
from .filters import TestFilter, CompletedTestsFilter, InProgressTestsFilter
from .serializers import TestListSerializer, CompletedTestSerializer, InProgressTestSerializer
from .pagination import CustomPagination
from apps.shared.models import get_main_topics
import json

class NotStartedTestListView(ListAPIView):
    serializer_class = TestListSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TestFilter
    ordering_fields = ['title', 'created_at', 'level', 'question_count']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        started_test_ids = Result.objects.filter(user=user).values_list('test_id', flat=True).distinct()
        #
        return Test.objects.filter(is_active=True).exclude(id__in=started_test_ids).annotate(
            question_count=Count('questions')
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # Añadir main_topics y total_by_level
        main_topics = get_main_topics()
        filtered_qs = self.filter_queryset(self.get_queryset())
        level_counts = filtered_qs.values('level').annotate(count=Count('id'))
        total_by_level = {item['level']: item['count'] for item in level_counts}

        response.data['data']['main_topics'] = main_topics
        response.data['stats']['total_by_level'] = total_by_level
        return response


class InProgressTestListView(ListAPIView):
    serializer_class = InProgressTestSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = InProgressTestsFilter
    ordering_fields = ['test__title', 'test__created_at', 'started_at', 'updated_at', 'time_taken']
    ordering = ['-updated_at']

    def get_queryset(self):
        user = self.request.user
        return Result.objects.filter(user=user, status='in_progress').select_related('test')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # Renombrar la clave de la lista a 'results'
        response.data['data']['results'] = response.data['data'].pop('tests')

        main_topics = get_main_topics()
        filtered_qs = self.filter_queryset(self.get_queryset())
        level_counts = filtered_qs.values('test__level').annotate(count=Count('id'))
        total_by_level = {item['test__level']: item['count'] for item in level_counts}

        response.data['data']['main_topics'] = main_topics
        response.data['stats']['total_by_level'] = total_by_level

        # Calcular estadísticas adicionales
        total_time = filtered_qs.aggregate(total=Sum('time_taken'))['total'] or 0
        total_answered = 0
        progress_sum = 0
        count = filtered_qs.count()
        for result in filtered_qs:
            answered = 0
            if result.answers:
                try:
                    answers = json.loads(result.answers) if isinstance(result.answers, str) else result.answers
                    answered = len(answers) if answers else 0
                except:
                    pass
            total_answered += answered
            total_q = result.test.questions.count()
            if total_q > 0:
                progress_sum += (answered / total_q) * 100
        avg_progress = (progress_sum / count) if count > 0 else 0

        response.data['stats']['average_progress'] = round(avg_progress, 2)
        response.data['stats']['total_questions_answered'] = total_answered
        response.data['stats']['total_time_spent'] = total_time

        return response


class CompletedTestListView(ListAPIView):
    serializer_class = CompletedTestSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CompletedTestsFilter
    ordering_fields = ['test__title', 'test__created_at', 'started_at', 'updated_at', 'time_taken', 'score']
    ordering = ['-updated_at']

    def get_queryset(self):
        user = self.request.user
        queryset = Result.objects.filter(user=user, status='completed').select_related('test')

        # Anotar posición de intento
        queryset = queryset.annotate(
            total_attempts=Window(
                expression=Count('id'),
                partition_by=[F('test_id')]
            ),
            attempt_position=Window(
                expression=Rank(),
                partition_by=[F('test_id')],
                order_by=[F('updated_at').asc(), F('id').asc()]
            )
        )

        # Anotar score para ordenar
        queryset = queryset.annotate(
            score=Coalesce(
                F('correct_answers') * 100.0 / (F('correct_answers') + F('wrong_answers')),
                Value(0.0),
                output_field=FloatField()
            )
        )
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # Renombrar la clave a 'test_results'
        response.data['data']['test_results'] = response.data['data'].pop('tests')

        main_topics = get_main_topics()
        filtered_qs = self.filter_queryset(self.get_queryset())
        level_counts = filtered_qs.values('test__level').annotate(count=Count('id'))
        total_by_level = {item['test__level']: item['count'] for item in level_counts}

        response.data['data']['main_topics'] = main_topics
        response.data['stats']['total_by_level'] = total_by_level

        # Estadísticas adicionales
        agg = filtered_qs.aggregate(
            avg_score=Avg('score'),
            total_time=Sum('time_taken'),
            total_questions=Sum(F('correct_answers') + F('wrong_answers'))
        )
        response.data['stats']['average_score'] = round(agg['avg_score'] or 0, 2)
        response.data['stats']['total_time_spent'] = agg['total_time'] or 0
        response.data['stats']['total_questions_answered'] = agg['total_questions'] or 0

        return response