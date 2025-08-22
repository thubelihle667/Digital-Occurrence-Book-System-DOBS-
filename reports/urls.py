from django.urls import path
from .views import SummaryView, TrendView, OccurrencesPDFView
from .views import TrendPNGView

urlpatterns = [
    path("summary/", SummaryView.as_view(), name="reports-summary"),
    path("trends/", TrendView.as_view(), name="reports-trends"),  # ?granularity=day|week|month
    path("occurrences.pdf", OccurrencesPDFView.as_view(), name="reports-occurrences-pdf"),
    path('trends.png', TrendPNGView.as_view(), name='reports-trends-png'),
]

