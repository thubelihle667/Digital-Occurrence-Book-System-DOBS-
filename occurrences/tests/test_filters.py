from django.urls import reverse
from rest_framework.test import APITestCase
from django.utils import timezone
from occurrences.models import Occurrence
from django.contrib.auth import get_user_model
from datetime import timedelta
from .factories import create_test_user

User = get_user_model()

class OccurrenceFilterTests(APITestCase):
    def setUp(self):
        self.user = create_test_user(email="alice@example.com", role="officer")
        self.client.force_authenticate(user=self.user)  # if your API requires auth
        now = timezone.now()

        Occurrence.objects.create(
            title="Gate break-in",
            description="...",
            location="Sandton",
            category="theft",
            occurred_at=now - timedelta(days=2),
            reported_by=self.user   
        )

        Occurrence.objects.create(
            title="Lost tag",
            description="...",
            location="Rosebank",
            category="lost",
            occurred_at=now - timedelta(days=10),
            reported_by=self.user  
        )

    def test_search_icontains(self):
        url = reverse("occurrence-list")
        res = self.client.get(url, {"search": "gate"})
        self.assertEqual(res.status_code, 200)
        titles = [x["title"] for x in res.data["results"]]
        self.assertIn("Gate break-in", titles)

    def test_date_range(self):
        url = reverse("occurrence-list")
        res = self.client.get(url, {"occurred_at_after": (timezone.now() - timedelta(days=5)).isoformat()})
        self.assertEqual(res.status_code, 200)
        titles = [x["title"] for x in res.data["results"]]
        self.assertIn("Gate break-in", titles)
        self.assertNotIn("Lost tag", titles)

    def test_location_filter(self):
        url = reverse("occurrence-list")
        res = self.client.get(url, {"location": "sand"})
        self.assertEqual(res.status_code, 200)
        titles = [x["title"] for x in res.data["results"]]
        self.assertIn("Gate break-in", titles)
