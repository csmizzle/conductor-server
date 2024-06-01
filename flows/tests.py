from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
import json


def get_flow_id(client: APIClient, flow_name: str):
    test_flow = None
    response = client.get(
        reverse("flow-deployments-list"),
    )
    for flow in response.json():
        if flow["name"] == flow_name:
            test_flow = flow["id"]
    return test_flow


class ReadFlowDeploymentsTest(TestCase):
    """Test module for GET all agent runs API"""

    def setUp(self):
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_all_deployment_runs(self):
        # get API response
        response = self.client.get(reverse("flow-deployments-list"))
        # get data from db
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FlowResultsTest(TestCase):
    """Test module for GET all agent runs API"""

    def setUp(self):
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.flow_data = {
            "flow_id": "1",
            "deployment_id": "1",
            "prefect_id": "1",
            "results": ["test"],
        }

    def test_get_all_flow_results(self):
        # get API response
        response = self.client.get(reverse("flow-results"))
        # get data from db
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_flow_results(self):
        # get API response
        response = self.client.post(
            reverse("flow-results"),
            data=json.dumps(self.flow_data),
            content_type="application/json",
        )
        # get data from db
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class DeployTestFlow(TestCase):
    """Test module for GET all agent runs API"""

    def setUp(self):
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_deploy_flow(self):
        test_flow = get_flow_id(self.client, "Test Flow")
        self.assertIsNotNone(test_flow)
        # deploy test flow
        deployed_flow_response = self.client.post(
            reverse("flow-deployments-create", kwargs={"deployment_id": test_flow}),
            data={"name": "Unit Test Flow"},
            format="json",
        )
        # get data from db
        print(deployed_flow_response.json())
        self.assertEqual(deployed_flow_response.status_code, status.HTTP_201_CREATED)


class ApolloMarketResearchFlowTest(TestCase):
    """Test module for GET all agent runs API"""

    def setUp(self):
        self.query = "Find me CTOs, CEOs in McLean, Va."
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_apollo_market_research_flow(self):
        test_flow = get_flow_id(self.client, "Market Research Flow")
        self.assertIsNotNone(test_flow)
        deployed_flow_response = self.client.post(
            reverse("flow-deployments-create", kwargs={"deployment_id": test_flow}),
            data={
                "name": "Unit Test Market Research Flow",
                "parameters": {"query": self.query},
            },
            format="json",
        )
        # get data from db
        print(deployed_flow_response.json())
        self.assertEqual(deployed_flow_response.status_code, status.HTTP_201_CREATED)
