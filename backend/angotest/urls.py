# angotest/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),   
    path('api/admin/', include('apps.admin_panel.urls')),   
    path('api/auth/', include('apps.accounts.urls')),
    path('api/user/', include('apps.accounts.user_urls')),
    path('api/test/', include('apps.test.urls')),
    path('api/results/', include('apps.results.urls')),
    path('api/rankings/', include('apps.rankings.urls')),
    path('api/invitations/', include('apps.invitations.urls')),
    path('api/ai-requests/', include('apps.ai.urls')),
    path('api/shared/', include('apps.shared.urls')),

]