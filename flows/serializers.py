from rest_framework import serializers
from flows import models


class FlowRunSerializer(serializers.Serializer):
    name = serializers.CharField()


class FlowResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FlowResult
        fields = "__all__"
