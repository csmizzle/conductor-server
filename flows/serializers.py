from rest_framework import serializers
from flows import models


class FlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Flow
        fields = ["prefect_id", "prefect_flow_id", "prefect_deployment_id"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        return models.Flow.objects.create(**validated_data)


class FlowRunSerializer(serializers.Serializer):
    name = serializers.CharField()
    parameters = serializers.JSONField()


class FlowResultInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FlowResult
        fields = ["flow", "results"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        return models.FlowResult.objects.create(**validated_data)


class FlowResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FlowResult
        fields = "__all__"


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
