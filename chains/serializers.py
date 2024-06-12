from rest_framework import serializers
from chains import models


class CreateChainSummarizeContentSerializer(serializers.Serializer):
    """Serializer for summarizing URLs"""

    content = serializers.ListField(
        child=serializers.CharField(),
        required=True,
        help_text="List of URLs to summarize",
    )
    flow_trace = serializers.IntegerField(
        required=False, help_text="ID of the flow to attach the event to"
    )


class ChainSummarySerializer(serializers.ModelSerializer):
    """
    Serializer for URL summary.
    """

    class Meta:
        model = models.Summary
        fields = "__all__"


class CreateApolloInputSerializer(serializers.Serializer):
    """Serializer for Apollo input"""

    flow_trace = serializers.IntegerField(
        required=False, help_text="ID of the flow to attach the event to"
    )
    query = serializers.CharField(required=True, max_length=5000)


class ChainEventSerializer(serializers.ModelSerializer):
    """
    Serializer for ChainEvent model.
    """

    class Meta:
        model = models.ChainEvent
        fields = "__all__"


class ChainTaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Celery task.
    """

    event = ChainEventSerializer(read_only=True)
    summary = ChainSummarySerializer(many=True, read_only=True)

    class Meta:
        model = models.ChainTask
        fields = "__all__"
        read_only_fields = ("task_id", "created_at", "status")


class ApolloContextInputChain(serializers.Serializer):
    """Serializer for Apollo context input"""

    flow_trace = serializers.IntegerField(
        required=False, help_text="ID of the flow to attach the event to"
    )
    person_titles = serializers.ListField(child=serializers.CharField(), required=True)
    person_locations = serializers.ListField(
        child=serializers.CharField(), required=True
    )


class ApolloUrlContextInputChain(serializers.Serializer):
    """Serializer for Apollo context URL input"""

    flow_trace = serializers.IntegerField(
        required=False, help_text="ID of the flow to attach the event to"
    )
    company_domains = serializers.ListField(
        child=serializers.CharField(),
        required=True,
        help_text="List of company URLs to get context for",
    )


class EmailFromContextSerializer(serializers.Serializer):
    """Serializer for creating email from context"""

    flow_trace = serializers.IntegerField(
        required=False, help_text="ID of the flow to attach the event to"
    )
    tone = serializers.CharField(required=True)
    context = serializers.CharField(required=True)
    sign_off = serializers.CharField(required=True)
