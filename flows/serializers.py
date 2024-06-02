from rest_framework import serializers

from flows import models


class FlowRunSerializer(serializers.Serializer):
    name = serializers.CharField()
    parameters = serializers.JSONField()


class FlowResultInputSerializer(serializers.Serializer):
    prefect_id = serializers.CharField()
    flow_id = serializers.CharField()
    deployment_id = serializers.CharField()
    results = serializers.JSONField()


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
