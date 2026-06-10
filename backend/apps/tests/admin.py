# apps/tests/admin.py
from django.contrib import admin

from .models import Test, Question, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    inlines = [AnswerInline]

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'main_topic', 'sub_topic', 'level', 'is_active', 'created_at']
    list_filter = ['level', 'is_active', 'main_topic']
    search_fields = ['title', 'description']
    inlines = [QuestionInline]

