from django.urls import path
from .views import SummaryView, TrendView, OccurrencesPDFView, ReportListView, ReportDetailView, TrendPNGView

urlpatterns = [
    path("summary/", SummaryView.as_view(), name="reports-summary"),
    path("trends/", TrendView.as_view(), name="reports-trends"),  # ?granularity=day|week|month
    path("occurrences.pdf", OccurrencesPDFView.as_view(), name="reports-occurrences-pdf"),
    path('trends.png', TrendPNGView.as_view(), name='reports-trends-png'),
    path("", ReportListView.as_view(), name="report-list"),
    path("<int:pk>/", ReportDetailView.as_view(), name="report-detail"),
]


