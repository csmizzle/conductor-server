from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from agents.models import AgentRun
from agents.serializers import AgentRunSerializer
import json
# Create your tests here.

client = Client()


class GetAllAgentRunsTest(TestCase):
    """ Test module for GET all agent runs API """

    def setUp(self):
        AgentRun.objects.create(task='Test Task', agent_name='Test Agent', output='Test Output')
        AgentRun.objects.create(task='Test Task 2', agent_name='Test Agent 2', output='Test Output 2')

    def test_get_all_agent_runs(self):
        # get API response
        response = client.get(reverse('agents'))
        # get data from db
        agent_runs = AgentRun.objects.all()
        serializer = AgentRunSerializer(agent_runs, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostAgentRunTest(TestCase):

    def setUp(self) -> None:
        self.valid_payload = {
            'task': 'Test Task',
            'agent_name': 'Test Agent',
            'output': 'Test Output'
        }
        self.invalid_payload = {
            'task': None,
            'agent_name': 'Test Agent',
            'output': 'Test Output'
        }

    def test_create_valid_agent_run(self):
        response = client.post(
            reverse('agents'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
