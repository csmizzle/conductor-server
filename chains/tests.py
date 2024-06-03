import json

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

client = Client()


class ApolloInputChainTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.valid_payload = {"query": "Find me CTOs, CEOs in McLean, Va."}
        self.invalid_payload = {"query": None}

    def test_create_valid_apollo_search(self):
        response = self.client.post(
            reverse("chains-apollo-input-list"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_apollo_search(self):
        response = self.client.post(
            reverse("chains-apollo-input-list"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ApolloInputFlowChainTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.flow_payload = {
            "flow_id": 1,
            "prefect_id": "test",
            "prefect_flow_id": "test",
            "prefect_deployment_id": "test",
        }
        self.query_payload = {"query": "Find me CTOs, CEOs in McLean, Va."}

    def test_create_valid_apollo_search(self):
        # create flow first
        response = self.client.post(
            reverse("flows-list"),
            data=json.dumps(self.flow_payload),
            content_type="application/json",
        )
        print(response.json())
        # attach query to flow
        self.query_payload["flow_id"] = response.json()["id"]
        response = self.client.post(
            reverse("chains-apollo-input-list"),
            data=json.dumps(self.query_payload),
            content_type="application/json",
        )
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
