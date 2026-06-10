# results/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Guardar/Actualizar resultado
    path('tests/<int:test_id>/save/', views.save_or_update_result, name='save_result'),
    
    # Obtener progreso
    path('tests/<int:test_id>/progress/', views.get_test_progress, name='get_test_progress'),
    
    # Eliminar progreso
    path('tests/<int:test_id>/progress/delete/', views.delete_test_progress, name='delete_test_progress'),
    
    # Lista de tests en progreso
    path('tests/in-progress/', views.get_my_in_progress_tests, name='in_progress_tests'),
    
    # Lista de tests completados
    path('tests/completed/', views.get_my_completed_tests, name='completed_tests'),
    
    # Obtener respuestas incorrectas
    path('results/<int:result_id>/incorrect-answers/', views.get_incorrect_answers, name='incorrect_answers'),
]