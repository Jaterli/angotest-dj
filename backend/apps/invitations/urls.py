# apps/invitations/urls.py
from django.urls import path
from .views import (
    CreateInvitationView,
    CheckInvitationView,
    AcceptInvitationView,
    AdminInvitationListView,
    AdminInvitationStatsView,
    AdminDeleteInvitationView,
    AdminDeleteInvitationsBulkView,
)

urlpatterns = [
    # Endpoints públicos (shared)
    path('create/', CreateInvitationView.as_view(), name='create_invitation'),
    path('check-invitation/', CheckInvitationView.as_view(), name='check_invitation'),
    path('accept-invitation/', AcceptInvitationView.as_view(), name='accept_invitation'),

    # Endpoints para el Admin
    path('admin/list/', AdminInvitationListView.as_view(), name='admin_invitations'),
    path('admin/stats/', AdminInvitationStatsView.as_view(), name='admin_invitation_stats'),
    path('admin/<int:invitation_id>/delete/', AdminDeleteInvitationView.as_view(), name='admin_delete_invitation'),
    path('admin/bulk-delete/', AdminDeleteInvitationsBulkView.as_view(), name='admin_delete_invitations_bulk'),


    # # Endpoints públicos (shared)
    # path('create/', _views.create_invitation, name='create_invitation'),
    # path('check-invitation/', _views.check_invitation, name='check_invitation'),
    # path('accept-invitation/', _views.accept_invitation, name='accept_invitation'),
    # path('my-invitations/', _views.get_user_invitations, name='user_invitations'),

    # # Endpoints para el Admin
    # path('admin/list/', _views.admin_get_invitations, name='admin_invitations'),
    # path('admin/stats/', _views.admin_get_invitation_stats, name='admin_invitation_stats'),
    # path('admin/<int:invitation_id>/', _views.admin_get_invitation_detail, name='admin_invitation_detail'),
    # path('admin/<int:invitation_id>/delete/', _views.admin_delete_invitation, name='admin_delete_invitation'),
    # path('admin/bulk-delete/', _views.admin_delete_invitations_bulk, name='admin_delete_invitations_bulk'),
]