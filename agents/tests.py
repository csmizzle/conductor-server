# Create your tests here.
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from agents.utils import run_url_marketing_report, save_pydantic_report
from reports.models import Report
from chains import models
import json
from conductor.reports.models import Report as PydanticReport
from conductor.reports.models import ReportStyle


class MarketingReportInputChainTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.valid_payload = {"url": "trssllc.com", "style": ReportStyle.BULLETED.name}
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
        self.url = "https://parenthetic.io"
        self.style = ReportStyle.BULLETED.name
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.event = models.ChainEvent.objects.create(
            created_by=self.user,
            chain_name=run_url_marketing_report.__name__,
            input=json.dumps({"url": self.url, "style": self.style}),
        )
        self.task = models.ChainTask.objects.create(
            created_by=self.user, event_id=self.event
        )

    def test_create_marketing_report(self):
        report = run_url_marketing_report(
            url=self.url,
            report_style=self.style,
            user_id=self.user.id,
            event_id=self.event.id,
            task_id=self.task.task_id,
        )
        assert isinstance(report, Report)


class SavePydanticReportTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.event = models.ChainEvent.objects.create(
            created_by=self.user,
            chain_name=run_url_marketing_report.__name__,
            input=json.dumps({"url": "trssllc.com"}),
        )
        self.task = models.ChainTask.objects.create(
            created_by=self.user, event_id=self.event
        )
        self.report = PydanticReport(
            **{
                "report": {
                    "title": "Test Report",
                    "description": "This is a test report",
                    "sections": [
                        {
                            "title": "Test Section",
                            "paragraphs": [
                                {
                                    "title": "Test Paragraph",
                                    "content": "This is a test paragraph",
                                },
                                {
                                    "title": "Test Paragraph",
                                    "content": "This is a test paragraph",
                                },
                            ],
                        }
                    ],
                },
                "style": ReportStyle.BULLETED,
                "raw": "This is a test report.",
            }
        )

    def test_save_pydantic_report(self) -> None:
        report = save_pydantic_report(
            pydantic_report=self.report,
            user=self.user,
            task=self.task,
        )
        print("Report", report.__dict__)
        assert isinstance(report, Report)
