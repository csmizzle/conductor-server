from rest_framework import views, status
from rest_framework.response import Response
from collect import serializers
from collect import models
from collect.tasks import task_collect_summarize_urls
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions


class SummarizeUrlsView(views.APIView):
    """Summarize URLs view"""

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=serializers.CreateSummarizeUrlsSerializer)
    def post(self, request, *args, **kwargs):
        """Summarize URLs"""
        request_serializer = serializers.CreateSummarizeUrlsSerializer(
            data=request.data
        )
        request_serializer.is_valid(raise_exception=True)
        task = models.Task.objects.create(created_by=request.user)
        task_collect_summarize_urls.delay(
            task_id=task.task_id, urls=request_serializer.validated_data["urls"]
        )
        task_serializer = serializers.TaskSerializer(task)
        return Response(task_serializer.data, status=status.HTTP_201_CREATED)
