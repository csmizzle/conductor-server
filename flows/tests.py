import json
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


def get_flow(client: APIClient, flow_name: str) -> dict:
    test_flow = None
    response = client.get(
        reverse("flow-deployments-list"),
    )
    for flow in response.json():
        if flow["name"] == flow_name:
            test_flow = flow
    return test_flow


def create_test_flow_trace_data(client: APIClient, flow_name: str) -> dict:
    # get data for flow trace
    test_flow = get_flow(client, flow_name)
    # create flow trace data
    flow_trace_data = {
        "prefect_flow_id": test_flow["flow_id"],
        "prefect_deployment_id": test_flow["id"],
        "prefect_name": flow_name,
    }
    # create flow trace
    created_flow_trace = client.post(
        reverse("flows-list"),
        data=json.dumps(flow_trace_data),
        content_type="application/json",
    )
    return created_flow_trace


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
        self.flow_name = "Test Flow"

    def test_get_all_flow_results(self):
        # get API response
        response = self.client.get(reverse("flow-results"))
        # get data from db
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_flow_results(self):
        test_flow_trace = create_test_flow_trace_data(self.client, self.flow_name)
        flow_results = {
            "flow_trace": test_flow_trace.json()["id"],
            "results": ["test"],
        }
        # get API response
        response = self.client.post(
            reverse("flow-results"),
            data=json.dumps(flow_results),
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
        self.flow_name = "Test Flow"

    def test_deploy_flow(self):
        # get data for flow trace
        test_flow = get_flow(self.client, self.flow_name)
        self.assertIsNotNone(test_flow)
        # create flow trace data
        flow_trace_data = {
            "prefect_flow_id": test_flow["flow_id"],
            "prefect_deployment_id": test_flow["id"],
            "prefect_name": self.flow_name,
        }
        # create flow trace
        created_flow_trace = self.client.post(
            reverse("flows-list"),
            data=json.dumps(flow_trace_data),
            content_type="application/json",
        )
        self.assertEqual(created_flow_trace.status_code, status.HTTP_201_CREATED)
        # deploy test flow from trace
        deployed_flow_response = self.client.post(
            reverse(
                "flow-deployments-create",
                kwargs={"flow_trace": created_flow_trace.json()["id"]},
            ),
        )
        # get data from db
        self.assertEqual(deployed_flow_response.status_code, status.HTTP_201_CREATED)


class ApolloMarketResearchFlowTest(TestCase):
    """Test module for GET all agent runs API"""

    def setUp(self):
        self.query = "Find me CTOs, CEOs in McLean, Va."
        self.user = User.objects.create_superuser(username="testowy", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.flow_name = "Market Research Flow"

    def test_apollo_market_research_flow(self):
        test_flow = get_flow(self.client, self.flow_name)
        self.assertIsNotNone(test_flow)
        # create flow trace data
        flow_trace_data = {
            "prefect_flow_id": test_flow["flow_id"],
            "prefect_deployment_id": test_flow["id"],
            "prefect_name": self.flow_name,
        }
        # create flow trace
        created_flow_trace = self.client.post(
            reverse("flows-list"),
            data=json.dumps(flow_trace_data),
            content_type="application/json",
        )
        deployed_flow_response = self.client.post(
            reverse(
                "flow-deployments-create",
                kwargs={"flow_trace": created_flow_trace.json()["id"]},
            ),
        )
        # get data from db
        self.assertEqual(deployed_flow_response.status_code, status.HTTP_201_CREATED)
