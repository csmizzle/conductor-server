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


class CreateApolloInputSerializer(serializers.Serializer):
    """Serializer for Apollo input"""

    query = serializers.CharField(required=True, max_length=5000)


class ChainEventSerializer(serializers.ModelSerializer):
    """
    Serializer for ChainEvent model.
    """

    class Meta:
        model = models.ChainEvent
        fields = "__all__"


class ApolloContextInputChain(serializers.Serializer):
    """Serializer for Apollo context input"""

    person_titles = serializers.ListField(child=serializers.CharField(), required=True)
    person_locations = serializers.ListField(
        child=serializers.CharField(), required=True
    )


class EmailFromContextSerializer(serializers.Serializer):
    """Serializer for creating email from context"""

    tone = serializers.CharField(required=True)
    context = serializers.CharField(required=True)
    sign_off = serializers.CharField(required=True)
