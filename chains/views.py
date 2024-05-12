from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from chains import serializers
from chains import models
from chains.tasks import run_summary_task


class ReadCreateModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    pass


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    """Task view set"""

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ChainTaskSerializer
    queryset = models.ChainTask.objects.all()
    lookup_field = "task_id"
    lookup_url_kwarg = "task_id"


class SummarizeContentViewSet(ReadCreateModelViewSet):
    """
    API endpoint that allows summaries to be created and retrieved.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ChainSummarySerializer
    queryset = models.Summary.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=serializers.CreateChainSummarizeContentSerializer,
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new summary.
        """
        request_serializer = serializers.CreateChainSummarizeContentSerializer(
            data=request.data
        )
        request_serializer.is_valid(raise_exception=True)
        task = models.ChainTask.objects.create(created_by=request.user)
        run_summary_task.delay(
            task_id=task.task_id, content=request_serializer.validated_data["content"]
        )
        task_serializer = serializers.ChainTaskSerializer(task)
        return Response(task_serializer.data, status=status.HTTP_201_CREATED)
