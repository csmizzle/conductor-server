"""
Pass through for the Prefect flows API.
"""
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import permissions
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from flows import serializers, models


class FlowRunApiView(APIView):
    """
    Flow API for Conductor flows
    """

    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

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

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=serializers.FlowResultInputSerializer,
    )
    def post(self, request: Request) -> Response:
        """
        Store the results of a flow run
        """
        input_serializer = serializers.FlowResultInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        result = models.FlowResult.objects.create(
            created_by=request.user,
            prefect_id=input_serializer.validated_data["prefect_id"],
            flow_id=input_serializer.validated_data["flow_id"],
            deployment_id=input_serializer.validated_data["deployment_id"],
            results=input_serializer.validated_data["results"],
        )
        result.save()
        result_serializer = serializers.FlowResultSerializer(result)
        # return the serialized result
        return Response(result_serializer.data, status=status.HTTP_201_CREATED)


class ReadFlowDeploymentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=serializers.ReadDeploymentInputSerializer,
    )
    def post(self, request: Request) -> Response:
        """
        Get all flow deployments
        """
        return Response(
            requests.post(
                f"{settings.PREFECT_API_URL}/deployments/filter",
                json=request.data,
            ).json(),
            status=status.HTTP_200_OK,
        )
