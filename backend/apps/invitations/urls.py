# apps/invitations/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Endpoints públicos (shared)
    path('create/', views.create_invitation, name='create_invitation'),
    path('check-invitation', views.check_invitation, name='check_invitation'),
    path('accept-invitation', views.accept_invitation, name='accept_invitation'),
    path('my-invitations/', views.get_user_invitations, name='user_invitations'),
]