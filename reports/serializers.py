"""
Report and paragraph serializers
"""
from rest_framework import serializers
from reports import models


class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Paragraph
        fields = ["title", "content"]

    def create(self, validated_data):
        user = self.context["request"].user
        paragraphs_data = validated_data.pop("paragraphs")
        validated_data["created_by"] = user
        report = models.Report.objects.create(**validated_data)
        for paragraph_data in paragraphs_data:
            paragraph_data["created_by"] = user
            models.Paragraph.objects.create(report=report, **paragraph_data)
        return report


class ReportSerializer(serializers.ModelSerializer):
    paragraphs = ParagraphSerializer(many=True)

    class Meta:
        model = models.Report
        fields = ["title", "description", "paragraphs"]

    def create(self, validated_data):
        user = self.context["request"].user
        paragraphs_data = validated_data.pop("paragraphs")
        validated_data["created_by"] = user
        report = models.Report.objects.create(**validated_data)
        for paragraph_data in paragraphs_data:
            paragraph_data["created_by"] = user
            models.Paragraph.objects.create(report=report, **paragraph_data)
        return report
