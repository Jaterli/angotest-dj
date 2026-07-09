import django_filters
from django.db.models import Q
from .models import Test
from apps.results.models import Result

class TestFilter(django_filters.FilterSet):
    main_topic = django_filters.CharFilter(field_name='main_topic', lookup_expr='exact')
    level = django_filters.CharFilter(field_name='level', lookup_expr='exact')
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Test
        fields = ['main_topic', 'level']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )


class CompletedTestsFilter(django_filters.FilterSet):
    main_topic = django_filters.CharFilter(field_name='test__main_topic', lookup_expr='exact')
    level = django_filters.CharFilter(field_name='test__level', lookup_expr='exact')
    search = django_filters.CharFilter(method='filter_search')
    from_date = django_filters.DateFilter(field_name='updated_at', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='updated_at', lookup_expr='lte')

    class Meta:
        model = Result
        fields = ['main_topic', 'level']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(test__title__icontains=value) |
            Q(test__description__icontains=value)
        )


class InProgressTestsFilter(django_filters.FilterSet):
    main_topic = django_filters.CharFilter(field_name='test__main_topic', lookup_expr='exact')
    level = django_filters.CharFilter(field_name='test__level', lookup_expr='exact')

    class Meta:
        model = Result
        fields = ['main_topic', 'level']