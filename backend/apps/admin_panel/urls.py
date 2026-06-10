# admin_panel/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Endpoints de Tests
    path('tests/all', views.get_all_tests, name='get_all_tests'),
    path('tests/create/', views.create_test, name='create_test'),
    path('tests/<int:test_id>/', views.get_test_by_id, name='get_test_by_id'),
    path('tests/<int:test_id>/edit/', views.update_test, name='update_test'),
    path('tests/<int:test_id>/delete/', views.delete_test, name='delete_test'),
    
    # Endpoints de Usuarios
    path('users/<int:user_id>/', views.get_user_by_id, name='get_user_by_id'),
    path('users/<int:user_id>/profile/', views.get_user_profile, name='get_user_profile'),
    path('users/<int:user_id>/update/', views.update_user, name='update_user'),
    path('users/stats/', views.get_users_with_stats, name='get_users_with_stats'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),

    # Endpoints de Resultados
    path('results/', views.get_results_list, name='get_results_list'),
    path('results/stats/', views.get_result_stats, name='get_result_stats'),
    path('results/<int:result_id>/', views.get_result_detail, name='get_result_detail'),
    path('results/<int:result_id>/delete/', views.delete_result, name='delete_result'),
    path('results/bulk-delete/', views.delete_results_bulk, name='delete_results_bulk'),
    path('results/export/csv/', views.export_results_csv, name='export_results_csv'),    

    # Endpoints de Invitaciones
    path('invitations/', views.admin_get_invitations, name='admin_invitations'),
    path('invitations/stats/', views.admin_get_invitation_stats, name='admin_invitation_stats'),
    path('invitations/<int:invitation_id>/', views.admin_get_invitation_detail, name='admin_invitation_detail'),
    path('invitations/<int:invitation_id>/delete/', views.admin_delete_invitation, name='admin_delete_invitation'),
    path('invitations/bulk-delete/', views.admin_delete_invitations_bulk, name='admin_delete_invitations_bulk'),

    # Endpoints de Cuotas de Usuario
    path('quotas/', views.admin_get_user_quotas, name='admin_get_user_quotas'),
    path('quotas/stats/', views.admin_get_quota_stats, name='admin_quota_stats'),
    path('quotas/create/', views.admin_create_user_quota, name='admin_create_quota'),
    path('quotas/bulk-delete/', views.admin_delete_quotas_bulk, name='admin_delete_quotas_bulk'),
    path('quotas/export/csv/', views.admin_export_quotas_csv, name='admin_export_quotas_csv'),
    path('quotas/<int:quota_id>/', views.admin_update_user_quota, name='admin_update_quota'),
    path('quotas/<int:quota_id>/delete/', views.admin_delete_user_quota, name='admin_delete_quota'),
    path('users/<int:user_id>/quotas/', views.admin_get_user_quota, name='admin_get_user_quota'),
    path('users/<int:user_id>/quota-months/', views.admin_get_user_quota_months, name='admin_user_quota_months'),    

    # Endpoints de Configuración del Sistema
    path('system-configs/', views.admin_get_system_configs, name='admin_get_system_configs'),
    path('system-configs/grouped/', views.admin_get_system_configs_grouped, name='admin_get_system_configs_grouped'),
    path('system-configs/export/csv/', views.admin_export_system_configs_csv, name='admin_export_system_configs_csv'),
    path('system-configs/bulk-update/', views.admin_bulk_update_system_configs, name='admin_bulk_update_system_configs'),
    path('system-configs/create/', views.admin_create_system_config, name='admin_create_system_config'),
    path('system-configs/key/<str:key>/', views.admin_get_system_config_by_key, name='admin_get_system_config_by_key'),
    #path('system-configs/by-prefix/<str:prefix>/', views.admin_get_system_configs_by_prefix, name='admin_get_system_configs_by_prefix'),
    path('system-configs/<int:config_id>/', views.admin_get_system_config, name='admin_get_system_config'),
    path('system-configs/update/<int:config_id>/', views.admin_update_system_config, name='admin_update_system_config'),
    path('system-configs/delete/<int:config_id>/', views.admin_delete_system_config, name='admin_delete_system_config'),    

    # Endpoints del Dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/activity-summary/', views.get_dashboard_activity_summary, name='dashboard_activity_summary'),
    path('dashboard/performance-metrics/', views.get_dashboard_performance_metrics, name='dashboard_performance_metrics'),
    path('dashboard/tests/<int:test_id>/stats/', views.get_test_detailed_stats, name='test_detailed_stats'),
    path('dashboard/users/<int:user_id>/stats/', views.get_user_detailed_stats, name='user_detailed_stats'),    

]