import django_filters as df
from .models import Occurrence

class OccurrenceFilter(df.FilterSet):
    # date range: ?occurred_at_after=2025-08-01&occurred_at_before=2025-08-25
    occurred_at_after = df.IsoDateTimeFilter(field_name="occurred_at", lookup_expr="gte")
    occurred_at_before = df.IsoDateTimeFilter(field_name="occurred_at", lookup_expr="lte")

    # location & category: exact/contains options
    location = df.CharFilter(field_name="location", lookup_expr="icontains")
    category = df.CharFilter(field_name="category", lookup_expr="iexact")  # or 'category__name' if FK

    class Meta:
        model = Occurrence
        fields = ["occurred_at_after", "occurred_at_before", "location", "category"]
