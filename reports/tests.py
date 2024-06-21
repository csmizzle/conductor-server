from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import json


class ReportInputChainTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.valid_payload = {
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
            "style": "BULLETED",
            "raw": "This is a test report.",
        }
        self.invalid_payload = {"title": None}

    def test_create_valid_report(self):
        response = self.client.post(
            reverse("reports-list"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # get list of reports
        response = self.client.get(reverse("reports-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invalid_report(self):
        response = self.client.post(
            reverse("reports-list"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReportToHtmlTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.payload = {
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
            "style": "as bulleted lists, avoiding long paragraphs.",
            "raw": "This is a test report.",
        }

    def test_report_to_html(self):
        response = self.client.post(
            reverse("reports-list"),
            data=json.dumps(self.payload),
            content_type="application/json",
        )
        report_id = response.data.get("id")
        response = self.client.get(
            reverse("generate-html", kwargs={"report_id": report_id}),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReportToPDFTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.payload = {
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
            "style": "as bulleted lists, avoiding long paragraphs.",
            "raw": "This is a test report.",
        }

    def test_report_to_html(self):
        response = self.client.post(
            reverse("reports-list"),
            data=json.dumps(self.payload),
            content_type="application/json",
        )
        report_id = response.data.get("id")
        response = self.client.get(
            reverse("generate-pdf", kwargs={"report_id": report_id}),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
