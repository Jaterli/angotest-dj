# tests/urls.py
from django.urls import path
from .views import (
    NotStartedTestListView, 
    InProgressTestListView, 
    CompletedTestListView, 
    TestDetailView, 
    TestProgressView, 
    SaveResultView, 
    DeleteTestProgressView, 
    NextQuestionView,
    AdminTestListView,
    AdminTestCreateView,
    AdminTestUpdateView,
    AdminTestDeleteView
)

urlpatterns = [
    
    path('not-started/', NotStartedTestListView.as_view(), name='not_started_tests'),
    path('in-progress/', InProgressTestListView.as_view(), name='in_progress_tests'),
    path('completed/', CompletedTestListView.as_view(), name='completed_tests'),

    path('<int:test_id>/', TestDetailView.as_view(), name='get_test_by_id'),

    # Lógica de negocio
    path('<int:test_id>/progress/', TestProgressView.as_view(), name='get_test_progress'),
    path('<int:test_id>/save/', SaveResultView.as_view(), name='save_result'),
    path('<int:test_id>/progress/delete/', DeleteTestProgressView.as_view(), name='delete_test_progress'),
    path('<int:test_id>/next-question/', NextQuestionView.as_view(), name='get_next_unanswered_question'),

    # Admin endpoints
    path('admin/list/', AdminTestListView.as_view(), name='get_all_tests'),
    path('admin/create/', AdminTestCreateView.as_view(), name='create_test'),
    path('admin/<int:test_id>/edit/', AdminTestUpdateView.as_view(), name='update_test'),
    path('admin/<int:test_id>/delete/', AdminTestDeleteView.as_view(), name='delete_test'),

    # # Tests
    # path('<int:test_id>/', views.get_test_by_id, name='get_test_by_id'),
    # path('<int:test_id>/save/', views.save_or_update_result, name='save_result'),
    # path('<int:test_id>/progress/', views.get_test_progress, name='get_test_progress'),
    # path('<int:test_id>/progress/delete/', views.delete_test_progress, name='delete_test_progress'),
    # path('not-started', views.get_not_started_tests, name='not_started_tests'),
    # path('in-progress', views.get_my_in_progress_tests, name='in_progress_tests'),
    # path('completed', views.get_my_completed_tests, name='completed_tests'),
    
    # # Preguntas
    # path('<int:test_id>/questions/', views.get_test_questions, name='get_test_questions'),
    # path('<int:test_id>/questions/<int:question_number>/', views.get_single_question, name='get_single_question'),
    # path('<int:test_id>/next-question/', views.get_next_unanswered_question, name='get_next_unanswered_question'),


    # # Admin Endpoints
    # path('admin/<int:test_id>/', views.get_test_by_id, name='get_test_by_id'),
    # path('admin/list/', views.get_all_tests, name='get_all_tests'),
    # path('admin/create/', views.create_test, name='create_test'),
    # path('admin/<int:test_id>/edit/', views.update_test, name='update_test'),
    # path('admin/<int:test_id>/delete/', views.delete_test, name='delete_test'),

]