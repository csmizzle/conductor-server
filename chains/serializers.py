from rest_framework import serializers
from chains import models


class CreateChainSummarizeContentSerializer(serializers.Serializer):
    """Serializer for summarizing URLs"""

    content = serializers.ListField(child=serializers.CharField(), required=True)


class ChainSummarySerializer(serializers.ModelSerializer):
    """
    Serializer for URL summary.
    """

    class Meta:
        model = models.Summary
        fields = "__all__"


class ChainTaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Celery task.
    """

    summary = ChainSummarySerializer(many=True, read_only=True)

    class Meta:
        model = models.ChainTask
        fields = "__all__"
        read_only_fields = ("task_id", "created_at", "status")
