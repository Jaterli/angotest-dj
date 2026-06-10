# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    
    # Dashboard
    path('dashboard/personaldata/', views.get_dashboard_data, name='dashboard_data'),
    path('dashboard/rankings/', views.get_rankings, name='rankings'),
]