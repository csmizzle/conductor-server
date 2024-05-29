"""
Pass through for the Prefect flows API.
"""
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class FlowRunApiView(APIView):
    """
    Flow API for Conductor flows
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="deployment_id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                description="The deployment ID of the flow to run",
                required=True,
            ),
            openapi.Parameter(
                name="",
                in_=openapi.IN_BODY,
                type=openapi.TYPE_STRING,
                description="The name of the flow run",
                required=True,
            ),
        ]
    )
    def post(self, request: Request) -> Response:
        return Response(
            requests.post(
                f"{settings.PREFECT_API_URL}/deployments/{request.query_params['deployment_id']}/create_flow_run",
                json=request.data,
            ).json(),
            status=status.HTTP_201_CREATED,
        )
