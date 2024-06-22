from rest_framework import serializers
from conductor.reports.models import ReportStyle
from agents import models


class URLMarketingCrewSerializer(serializers.Serializer):
    url = serializers.CharField()
    style = serializers.ChoiceField(
        choices=[(style.name, style.value) for style in ReportStyle]
    )


class CrewTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CrewTask
        fields = ["id", "agent_role", "description", "output"]

    def create(self, validated_data) -> models.CrewTask:
        user = self.context["request"].user
        validated_data["created_by"] = user
        crew_task = models.CrewTask.objects.create(**validated_data)
        return crew_task


class CrewRunSerializer(serializers.ModelSerializer):
    tasks = CrewTaskSerializer(many=True)

    class Meta:
        model = models.CrewRun
        fields = ["id", "tasks", "result"]

    def create(self, validated_data) -> models.CrewRun:
        user = self.context["request"].user
        tasks_data = validated_data.pop("tasks")
        crew_run = models.CrewRun.objects.create(**validated_data)
        for task_entry in tasks_data:
            task_entry["created_by"] = user
            task = models.CrewTask.objects.create(**task_entry)
            crew_run.tasks.add(task)
        return crew_run
