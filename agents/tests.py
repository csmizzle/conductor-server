# Create your tests here.
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from agents.utils import (
    run_url_marketing_report,
    save_pydantic_report,
    save_pydantic_crew_run,
)
from reports.models import Report
from agents import models as agent_models
from chains import models
import json
from conductor.reports.models import Report as PydanticReport
from conductor.reports.models import ReportStyle
from conductor.crews.models import CrewRun as PydanticCrewRun


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
        assert report.report is not None
        assert report.style == ReportStyle.BULLETED.value
        assert report.raw is not None
        assert isinstance(report.crew_run, agent_models.CrewRun)


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
        assert isinstance(report, Report)
        # make sure enum serialized correctly
        assert report.style == ReportStyle.BULLETED.value


class SaveCrewRunTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.crew_run = PydanticCrewRun(
            **{
                "task_outputs": [
                    {
                        "description": "test description",
                        "summary": "test summary",
                        "exported_output": "test exported output",
                        "raw_output": "test raw output",
                    },
                    {
                        "description": "test description",
                        "summary": "test summary",
                        "exported_output": "test exported output",
                        "raw_output": "test raw output",
                    },
                ],
                "result": "this is a test results",
            }
        )

    def test_save_crew_run(self) -> None:
        crew_run = save_pydantic_crew_run(
            pydantic_crew_run=self.crew_run,
            user=self.user,
        )
        assert isinstance(crew_run, agent_models.CrewRun)
        assert crew_run.tasks.count() == 2
        response = self.client.get(
            reverse("runs-list"),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
