from rest_framework import serializers

from agents.models import AgentRun


class AgentInput(serializers.Serializer):
    """
    Serializer for the agent input
    """

    task = serializers.CharField(max_length=300)


class AgentRunSerializer(serializers.ModelSerializer):
    """
    Serializer for the agent output
    """

    class Meta:
        model = AgentRun
        fields = ["task", "agent_name", "output"]
