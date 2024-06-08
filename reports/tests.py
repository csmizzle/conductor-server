from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import json

client = Client()


class ReportInputChainTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.valid_payload = {
            "title": "Test Report",
            "description": "This is a test report",
            "paragraphs": [
                {"title": "Test Paragraph", "content": "This is a test paragraph"}
            ],
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


# class ReportToHtmlTest(TestCase):

#     def setUp(self) -> None:
#         self.user = User.objects.create_superuser(username="testowy", password="test")
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
#         self.payload = {
#             "title": "Test Report",
#             "description": "This is a test report",
#             "paragraphs": [
#                 {"title": "Test Paragraph", "content": "This is a test paragraph"}
#             ],
#         }

#     def test_report_to_html(self):
#         response = self.client.post(
#             reverse("reports-list"),
#             data=json.dumps(self.payload),
#             content_type="application/json",
#         )
#         report_id = response.data.get("id")
#         response = self.client.get(
#             reverse("generate-report-html", kwargs={"report_id": report_id}),
#         )
#         print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
