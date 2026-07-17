import django_filters # type: ignore
from django.db.models import Q
from django.utils import timezone
from .models import TestInvitation

class InvitationFilter(django_filters.FilterSet):
    invited_by = django_filters.NumberFilter(field_name='invited_by_id')
    is_used = django_filters.BooleanFilter(field_name='is_used')
    is_guest = django_filters.BooleanFilter(field_name='is_guest')
    status = django_filters.ChoiceFilter(method='filter_status', choices=[
        ('active', 'Active'),
        ('used', 'Used'),
        ('expired', 'Expired'),
    ])
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = TestInvitation
        fields = ['invited_by', 'is_used', 'is_guest', 'status', 'start_date', 'end_date']

    def filter_status(self, queryset, name, value):
        now = timezone.now()
        if value == 'active':
            return queryset.filter(is_used=False, expires_at__gt=now)
        elif value == 'used':
            return queryset.filter(is_used=True)
        elif value == 'expired':
            return queryset.filter(is_used=False, expires_at__lte=now)
        return queryset