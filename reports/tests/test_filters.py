from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from reports.models import Report
from reports.filters import ReportFilter

User = get_user_model()


class ReportFilterTests(TestCase):
    def setUp(self):
        now = timezone.now()
        self.user = User.objects.create_user(
            username="bob",
            email="bob@example.com",
            role="ADMIN",
            password="pass1234"
        )

        self.report1 = Report.objects.create(
            title="Weekly Theft Report",
            location="Downtown",
            category="Theft",
            created_by=self.user,
            created_at=now - timedelta(days=2)
        )
        self.report2 = Report.objects.create(
            title="Monthly Fraud Report",
            location="Uptown",
            category="Fraud",
            created_by=self.user,
            created_at=now - timedelta(days=30)
        )
        self.report3 = Report.objects.create(
            title="Daily Incident Report",
            location="Downtown",
            category="Incident",
            created_by=self.user,
            created_at=now - timedelta(days=1)
        )

    def test_date_range(self):
        now_dt = timezone.now()
        date_from = (now_dt - timedelta(days=7)).isoformat()
        date_to = now_dt.isoformat()

        reports = ReportFilter(
            {'date_from': date_from, 'date_to': date_to},
            queryset=Report.objects.all()
        ).qs

        # Only report1 and report3 should be included
        self.assertIn(self.report1, reports)
        self.assertIn(self.report3, reports)
        self.assertNotIn(self.report2, reports)
