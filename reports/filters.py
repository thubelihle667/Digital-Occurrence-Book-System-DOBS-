import django_filters
from reports.models import Report

class ReportFilter(django_filters.FilterSet):
    date_from = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    date_to = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Report
        fields = ['date_from', 'date_to', 'location', 'search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(title__icontains=value)
