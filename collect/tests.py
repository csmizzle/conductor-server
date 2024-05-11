from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
import json


class PostSummarizeUrlsTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_post_summarize_urls(self):
        url = reverse("collect_summarize_urls")
        data = {
            "urls": [
                "https://webscraper.io/test-sites/e-commerce/ajax",
            ]
        }
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
