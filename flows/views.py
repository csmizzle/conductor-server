"""
Pass through for the Prefect flows API.
"""
import requests
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from flows import models, serializers


class FlowTraceViewSet(viewsets.ModelViewSet):
    """
    Create and list flows for execution in Prefect
    """

    queryset = models.FlowTrace.objects.all()
    serializer_class = serializers.FlowTraceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)


class FlowRunApiView(APIView):
    """
    Flow API for Conductor flows in prefect
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="flow_trace",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                description="The deployment ID of the flow trace to run",
                required=True,
            ),
        ],
    )
    def post(self, request: Request, flow_trace: str) -> Response:
        flow = (
            models.FlowTrace.objects.all()
            .filter(created_by=request.user, id=flow_trace)
            .first()
        )
        if flow:
            created_deployment = requests.post(
                f"{settings.PREFECT_API_URL}/deployments/{flow.prefect_deployment_id}/create_flow_run",
                json={
                    "name": flow.prefect_name,
                    "parameters": flow.prefect_parameters
                    if flow.prefect_parameters
                    else {},
                },
            )
            if created_deployment.ok:
                return Response(
                    created_deployment.json(),
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    created_deployment.json(),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"msg": "Flow not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class FlowResultView(APIView):
    """
    Store the results of the flow run
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        """
        Get all flow results
        """
        results = serializers.FlowResultSerializer(
            models.FlowResult.objects.all().filter(created_by=request.user), many=True
        )
        return Response(results.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=serializers.FlowResultSerializer,
    )
    def post(self, request: Request) -> Response:
        """
        Store the results of a flow run
        """
        input_serializer = serializers.FlowResultSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        flow_trace = (
            models.FlowTrace.objects.all()
            .filter(id=input_serializer.validated_data["flow_trace"].id)
            .first()
        )
        if flow_trace:
            result = models.FlowResult.objects.create(
                created_by=request.user,
                flow_trace=input_serializer.validated_data["flow_trace"],
                results=input_serializer.validated_data["results"],
            )
            result.save()
            result_serializer = serializers.FlowResultSerializer(result)
            # return the serialized result
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"msg": "Flow not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class ReadFlowDeploymentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        """
        Get all flow deployments
        """
        return Response(
            requests.post(
                f"{settings.PREFECT_API_URL}/deployments/filter",
            ).json(),
            status=status.HTTP_200_OK,
        )
