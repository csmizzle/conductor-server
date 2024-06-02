from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response

from collect import models, serializers
from collect.tasks import task_collect_summarize_urls


class ReadCreateModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    pass


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    """Task view set"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.TaskSerializer
    queryset = models.Task.objects.all()
    lookup_field = "task_id"
    lookup_url_kwarg = "task_id"


class URLSummaryViewSet(ReadCreateModelViewSet):
    """URL summary view set"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.URLSummarySerializer
    queryset = models.URLSummary.objects.all()
    lookup_field = "job_id"
    lookup_url_kwarg = "job_id"

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CreateSummarizeUrlsSerializer
        return serializers.URLSummarySerializer

    @swagger_auto_schema(
        request_body=serializers.CreateSummarizeUrlsSerializer,
        responses={status.HTTP_201_CREATED: serializers.TaskSerializer},
    )
    def create(self, request, *args, **kwargs):
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
