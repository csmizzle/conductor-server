from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
import json


client = Client()


class PostApolloSearchTest(TestCase):

    def setUp(self) -> None:
        self.valid_payload = {
            'query': 'Who are the key players?'
        }
        self.invalid_payload = {
            'query': None
        }

    def test_create_valid_apollo_search(self):
        response = client.post(
            reverse('search_apollo'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invalid_apollo_search(self):
        response = client.post(
            reverse('search_apollo'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)