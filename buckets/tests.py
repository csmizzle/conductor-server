from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class GetBucketsTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_task(self):
        url = reverse("buckets")
        response = self.client.get(url, QUERY_STRING="bucket_name=discord-bucket-dev")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetBucketsObjectTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_bucket_object(self):
        url = reverse("buckets-object")
        response = self.client.get(
            url,
            QUERY_STRING="bucket_name=discord-bucket-dev&object_name=1233762364923445309%2F32cb30e9-2772-4154-901e-24c0af76640f.json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetBucketsObjectLatestTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_bucket_object_latest(self):
        url = reverse("buckets-object-latest")
        response = self.client.get(url, QUERY_STRING="bucket_name=discord-bucket-dev")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
