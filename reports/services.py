from datetime import datetime
from io import BytesIO
from typing import Tuple, Dict, Any, List

from django.db.models import Count, Q
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.utils import timezone

from occurrences.models import Occurrence  

# ---- filtering helpers ----
def _parse_date(s: str):
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None

def filtered_occurrences(params) -> Tuple[Any, str]:
    """
    Filters occurrences by query params:
    ?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD&status=open&severity=high&category=...
    """
    qs = Occurrence.objects.all()

    # Choose primary date field
    date_field = "occurred_at" if hasattr(Occurrence, "occurred_at") else "created_at"

    date_from = _parse_date(params.get("date_from", "")) or None
    date_to   = _parse_date(params.get("date_to", "")) or None

    if date_from:
        filter_key = f"{date_field}__date__gte"
        qs = qs.filter(**{filter_key: date_from.date()})
    if date_to:
        filter_key = f"{date_field}__date__lte"
        qs = qs.filter(**{filter_key: date_to.date()})

    if status := params.get("status"):
        qs = qs.filter(status=status)
    if severity := params.get("severity"):
        qs = qs.filter(severity=severity)
    if category := params.get("category"):
        qs = qs.filter(category=category)
    if reporter := params.get("reported_by"):
        qs = qs.filter(reported_by__username=reporter)  # or ID

    return qs, date_field

# ---- summaries ----
def summary_counts(qs) -> Dict[str, int]:
    return qs.aggregate(
        total=Count("id"),
        open=Count("id", filter=Q(status="open")),
        in_progress=Count("id", filter=Q(status="in_progress")),
        closed=Count("id", filter=Q(status="closed")),
        sev_low=Count("id", filter=Q(severity="low")),
        sev_medium=Count("id", filter=Q(severity="medium")),
        sev_high=Count("id", filter=Q(severity="high")),
    )

def time_series(qs, date_field: str, granularity: str = "month") -> List[Dict[str, Any]]:
    if granularity == "day":
        trunc = TruncDay(date_field)
    elif granularity == "week":
        trunc = TruncWeek(date_field)
    else:
        trunc = TruncMonth(date_field)

    data = (
        qs.annotate(bucket=trunc)
          .values("bucket")
          .annotate(count=Count("id"))
          .order_by("bucket")
    )
    return [{"bucket": r["bucket"], "count": r["count"]} for r in data]
