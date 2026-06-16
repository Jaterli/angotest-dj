# ai/models.py
from django.db import models
from django.conf import settings

class AIRequestLog(models.Model):
    """Modelo para registrar solicitudes de generación de tests con IA"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_requests')
    test = models.ForeignKey('test.Test', on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_requests')
    
    main_topic = models.CharField(max_length=255, blank=True)
    sub_topic = models.CharField(max_length=255, blank=True)
    specific_topic = models.CharField(max_length=255, blank=True)
    level = models.CharField(max_length=20)
    num_questions = models.IntegerField()
    num_answers = models.IntegerField()
    language = models.CharField(max_length=2, default='es')
    generation_mode = models.CharField(max_length=20, default='guided')
    ai_prompt = models.TextField(blank=True)
    
    # Respuesta de la IA
    ai_response = models.JSONField(default=dict, blank=True)
    ai_provider = models.CharField(max_length=50, blank=True)
    ai_model = models.CharField(max_length=100, blank=True)
    
    # Estado
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pendiente'),
        ('completed', 'Completado'),
        ('failed', 'Fallido'),
    ])
    error_message = models.TextField(blank=True)
    
    # Métricas
    response_time = models.FloatField(default=0)  # en segundos
    tokens_used = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ai_request_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['generation_mode']),
        ]
    
    def __str__(self):
        return f"AI Request {self.pk} - {self.user.username} - {self.status}"