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
from flows import serializers, models


class FlowRunApiView(APIView):
    """
    Flow API for Conductor flows
    """

    @swagger_auto_schema(
        request_body=serializers.FlowRunSerializer,
        manual_parameters=[
            openapi.Parameter(
                name="deployment_id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                description="The deployment ID of the flow to run",
                required=True,
            ),
        ],
    )
    def post(self, request: Request, deployment_id: str) -> Response:
        return Response(
            requests.post(
                f"{settings.PREFECT_API_URL}/deployments/{deployment_id}/create_flow_run",
                json=request.data,
            ).json(),
            status=status.HTTP_201_CREATED,
        )


class FlowResultListView(APIView):
    def get(self, request: Request) -> Response:
        """
        Get all flow results
        """
        results = serializers.FlowResultSerializer(
            models.FlowResult.objects.all(), many=True
        )
        return Response(results.data, status=status.HTTP_200_OK)


class FlowResultView(APIView):
    """
    Store the results of the flow run
    """

    @swagger_auto_schema(
        request_body=serializers.FlowResultSerializer,
    )
    def post(self, request: Request) -> Response:
        """
        Store the results of a flow run
        """
        result = models.FlowResult.objects.create(
            user=request.user,
            context=request.data["context"],
            result=request.data["result"],
        )
        result_serializer = serializers.FlowResultSerializer(result)
        # return the serialized run
        return Response(result_serializer.data, status=status.HTTP_201_CREATED)
