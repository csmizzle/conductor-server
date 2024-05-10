from rest_framework import views, status
from rest_framework.response import Response
from collect.serializers import CreateSummarizeUrlsSerializer
from collect.tasks import task_collect_summarize_urls
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions


class SummarizeUrlsView(views.APIView):
    """Summarize URLs view"""

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=CreateSummarizeUrlsSerializer)
    def post(self, request, *args, **kwargs):
        """Summarize URLs"""
        request_serializer = CreateSummarizeUrlsSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        task_collect_summarize_urls.delay(request_serializer.validated_data["urls"])
        return Response({"msg": "Collect task started!"}, status=status.HTTP_200_OK)
