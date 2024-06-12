from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from agents.serializers import URLMarketingCrewSerializer
from agents.tasks import run_marketing_report_task
from chains import models as chain_models
from chains import serializers as chain_serializers
import json


class URLMarketingCrewView(APIView):
    """
    Expose marketing crew to create marketing reports
    """

    @swagger_auto_schema(
        request_body=URLMarketingCrewSerializer,
        operation_description="Create a marketing report",
    )
    def post(self, request: Request) -> Response:
        request_serializer = URLMarketingCrewSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        # create chain event
        event = chain_models.ChainEvent.objects.create(
            flow_trace=None,
            created_by=request.user,
            chain_name=run_marketing_report_task.__name__,
            input=json.dumps(request_serializer.validated_data),
        )
        task = chain_models.ChainTask.objects.create(
            created_by=request.user, event_id=event
        )
        run_marketing_report_task.delay(
            url=request_serializer.validated_data["url"],
            user_id=request.user.id,
            task_id=task.task_id,
            event_id=event.id,
        )
        task_serializer = chain_serializers.ChainTaskSerializer(task)
        return Response(task_serializer.data, status=status.HTTP_201_CREATED)
