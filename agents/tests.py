# Create your tests here.
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from agents.utils import run_url_marketing_report
from reports.models import Report
from chains import models
import json


class MarketingReportInputChainTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.valid_payload = {"url": "trssllc.com"}
        self.invalid_payload = {"url": None}

    def test_create_valid_report(self):
        response = self.client.post(
            reverse("marketing-report"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_report(self):
        response = self.client.post(
            reverse("marketing-report"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MarketingReportTestCase(TestCase):
    def setUp(self) -> None:
        self.url = "https://trssllc.com"
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.event = models.ChainEvent.objects.create(
            created_by=self.user,
            chain_name=run_url_marketing_report.__name__,
            input=json.dumps({"url": self.url}),
        )
        self.task = models.ChainTask.objects.create(
            created_by=self.user, event_id=self.event
        )

    def test_create_marketing_report(self):
        report = run_url_marketing_report(
            url=self.url,
            user_id=self.user.id,
            event_id=self.event.id,
            task_id=self.task.task_id,
        )
        assert isinstance(report, Report)
