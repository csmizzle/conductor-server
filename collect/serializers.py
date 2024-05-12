from rest_framework import serializers
from collect import models


class CreateSummarizeUrlsSerializer(serializers.Serializer):
    """Serializer for summarizing URLs"""

    urls = serializers.ListField(child=serializers.CharField(), required=True)


class URLSummarySerializer(serializers.ModelSerializer):
    """
    Serializer for URL summary.
    """

    class Meta:
        model = models.URLSummary
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Celery task.
    """

    url_summary = URLSummarySerializer(many=True, read_only=True)

    class Meta:
        model = models.Task
        fields = "__all__"
        read_only_fields = ("task_id", "created_at", "status")
