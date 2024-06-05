from rest_framework import serializers
from flows import models
from chains import serializers as chains_serializers


class FlowRunSerializer(serializers.Serializer):
    flow_trace = serializers.IntegerField(required=True)


class FlowResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FlowResult
        fields = ["flow_trace", "results"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        return models.FlowResult.objects.create(**validated_data)


class FlowTraceSerializer(serializers.ModelSerializer):
    events = chains_serializers.ChainEventSerializer(many=True, read_only=True)
    results = FlowResultSerializer(many=True, read_only=True)

    class Meta:
        model = models.FlowTrace
        fields = [
            "id",
            "prefect_flow_id",
            "prefect_deployment_id",
            "prefect_name",
            "prefect_parameters",
            "events",
            "results",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        return models.FlowTrace.objects.create(**validated_data)


class FlowFilterSerializer(serializers.Serializer):
    operator = serializers.CharField(required=False)
    id = serializers.CharField(required=False)
    deployment = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)


class ReadDeploymentInputSerializer(serializers.Serializer):
    offset = serializers.IntegerField(default=0)
    flows = FlowFilterSerializer(required=False)
    sort = serializers.ChoiceField(
        choices=["CREATED_DESC", "UPDATED_DESC", "NAME_ASC", "NAME_DESC"],
        default="NAME_ASC",
    )


class FlowTraceRunSerializer(serializers.Serializer):
    prefect_deployment_id = serializers.CharField(required=False)
    prefect_name = serializers.CharField(required=False)
    prefect_parameters = serializers.JSONField(required=False, default={})
