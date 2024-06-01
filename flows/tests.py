from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse


class ReadFlowDeploymentsTest(TestCase):
    """Test module for GET all agent runs API"""

    def setUp(self):
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_all_deployment_runs(self):
        # get API response
        response = self.client.post(reverse("flow-deployments"))
        # get data from db
        self.assertEqual(response.status_code, status.HTTP_200_OK)
