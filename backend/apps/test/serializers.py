from rest_framework import serializers
from .models import Test
from apps.results.models import Result
import json

class TestListSerializer(serializers.ModelSerializer):
    total_questions = serializers.IntegerField(source='question_count', read_only=True)

    class Meta:
        model = Test
        fields = [
            'id', 'title', 'description', 'main_topic', 'sub_topic',
            'specific_topic', 'level', 'is_active', 'created_by',
            'created_at', 'updated_at', 'total_questions'
        ]


class CompletedTestSerializer(serializers.ModelSerializer):
    test_title = serializers.CharField(source='test.title')
    test_description = serializers.CharField(source='test.description')
    test_main_topic = serializers.CharField(source='test.main_topic')
    test_sub_topic = serializers.CharField(source='test.sub_topic')
    test_specific_topic = serializers.CharField(source='test.specific_topic')
    test_level = serializers.CharField(source='test.level')
    test_created_at = serializers.DateTimeField(source='test.created_at')
    total_questions = serializers.IntegerField(source='test.questions.count', read_only=True)
    score_percent = serializers.SerializerMethodField()
    score_rounded = serializers.SerializerMethodField()
    attempt_position = serializers.IntegerField(read_only=True)
    total_attempts = serializers.IntegerField(read_only=True)

    class Meta:
        model = Result
        fields = [
            'id', 'user_id', 'test_id', 'correct_answers', 'wrong_answers',
            'time_taken', 'status', 'started_at', 'updated_at',
            'test_title', 'test_description', 'test_main_topic', 'test_sub_topic',
            'test_specific_topic', 'test_level', 'test_created_at',
            'total_questions', 'score_percent', 'score_rounded',
            'attempt_position', 'total_attempts'
        ]

    def get_score_percent(self, obj):
        total = obj.correct_answers + obj.wrong_answers
        if total == 0:
            return 0.0
        return round((obj.correct_answers / total) * 100, 2)

    def get_score_rounded(self, obj):
        total = obj.correct_answers + obj.wrong_answers
        if total == 0:
            return 0
        return round((obj.correct_answers / total) * 100)


class InProgressTestSerializer(serializers.ModelSerializer):
    test_title = serializers.CharField(source='test.title')
    test_description = serializers.CharField(source='test.description')
    test_main_topic = serializers.CharField(source='test.main_topic')
    test_sub_topic = serializers.CharField(source='test.sub_topic')
    test_specific_topic = serializers.CharField(source='test.specific_topic')
    test_level = serializers.CharField(source='test.level')
    test_created_at = serializers.DateTimeField(source='test.created_at')
    total_questions = serializers.IntegerField(source='test.questions.count', read_only=True)
    answered_count = serializers.SerializerMethodField()
    remaining_count = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Result
        fields = [
            'id', 'user_id', 'test_id', 'time_taken', 'status',
            'started_at', 'updated_at',
            'test_title', 'test_description', 'test_main_topic', 'test_sub_topic',
            'test_specific_topic', 'test_level', 'test_created_at',
            'total_questions', 'answered_count', 'remaining_count', 'progress'
        ]

    def get_answered_count(self, obj):
        if obj.answers:
            try:
                answers = json.loads(obj.answers) if isinstance(obj.answers, str) else obj.answers
                return len(answers) if answers else 0
            except:
                return 0
        return 0

    def get_remaining_count(self, obj):
        total = self.get_total_questions(obj)
        answered = self.get_answered_count(obj)
        return max(0, total - answered)

    def get_progress(self, obj):
        total = self.get_total_questions(obj)
        if total == 0:
            return 0.0
        answered = self.get_answered_count(obj)
        return round((answered / total) * 100, 2)

    def get_total_questions(self, obj):
        return obj.test.questions.count()