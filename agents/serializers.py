from rest_framework import serializers
from conductor.reports.models import ReportStyle


class URLMarketingCrewSerializer(serializers.Serializer):
    url = serializers.CharField()
    style = serializers.ChoiceField(
        choices=[(style.name, style.value) for style in ReportStyle]
    )
