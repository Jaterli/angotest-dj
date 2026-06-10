# tests/models.py
from django.db import models


class Test(models.Model):
    LEVEL_CHOICES = (
        ('Principiante', 'Principiante'),
        ('Intermedio', 'Intermedio'),
        ('Avanzado', 'Avanzado'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    main_topic = models.CharField(max_length=255, default='General')
    sub_topic = models.CharField(max_length=255, default='General')
    specific_topic = models.CharField(max_length=255, default='General')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='tests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'tests'
        indexes = [
            models.Index(fields=['main_topic', 'sub_topic']),
            models.Index(fields=['level']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def total_questions(self):
        return self.questions.count()


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    
    class Meta:
        db_table = 'questions'
    
    def __str__(self):
        return self.question_text[:50]

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'answers'
    
    def __str__(self):
        return self.answer_text[:50]
    