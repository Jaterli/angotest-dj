# results/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Usuarios o compartido
    path('<int:result_id>/incorrect-answers/', views.get_incorrect_answers, name='incorrect_answers'),

    # # Admin
    path('', views.get_results_list, name='get_results_list'),
    path('user/<int:user_id>/', views.get_user_results, name='admin_user_results'),
    path('<int:result_id>/user/<int:user_id>/', views.get_user_result_details, name='admin_user_result_details'),
    path('<int:result_id>/delete/', views.delete_result, name='delete_result'),
    path('bulk-delete/', views.delete_results_bulk, name='delete_results_bulk'),
    path('stats/', views.get_result_stats, name='get_result_stats'),
    path('<int:result_id>/', views.get_result_detail, name='get_result_detail'),
    path('export-csv/', views.export_results_csv, name='export_results_csv'),
]