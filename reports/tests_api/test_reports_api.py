from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from occurrences.models import Occurrence

User = get_user_model()

class ReportsAPITests(APITestCase):
    def setUp(self):
        # Include required fields for custom user model
        self.user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            role="USER",   # match the role choices in your model
            password="pass123"
        )
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            role="ADMIN",  # match your role for superuser
            password="pass123"
        )
        self.client = APIClient()

        now = timezone.now()
        Occurrence.objects.create(
            title="A",
            status="open",
            severity="low",
            reported_by=self.user,
            created_at=now
        )
        Occurrence.objects.create(
            title="B",
            status="closed",
            severity="high",
            reported_by=self.user,
            created_at=now
        )

    def test_summary_requires_auth(self):
        url = reverse("reports-summary")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 401)

    def test_summary_ok(self):
        self.client.force_authenticate(self.user)
        url = reverse("reports-summary")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIn("total", res.data)
        self.assertIn("open", res.data)
        self.assertIn("closed", res.data)

    def test_trends_ok(self):
        self.client.force_authenticate(self.user)
        url = reverse("reports-trends") + "?granularity=month"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, list)

    def test_pdf_admin_only(self):
        url = reverse("reports-occurrences-pdf")
        # unauth
        res = self.client.get(url)
        self.assertEqual(res.status_code, 401)

        # non-admin
        self.client.force_authenticate(self.user)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 403)

        # admin
        self.client.force_authenticate(self.admin)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res["Content-Type"], "application/pdf")
