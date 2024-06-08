"""
Report and paragraph serializers
"""
from rest_framework import serializers
from reports import models


class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Paragraph
        fields = ["id", "title", "content"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        paragraph = models.Paragraph.objects.create(**validated_data)
        return paragraph


class ReportSerializer(serializers.ModelSerializer):
    paragraphs = ParagraphSerializer(many=True)

    class Meta:
        model = models.Report
        fields = ["id", "title", "description", "paragraphs"]

    def create(self, validated_data):
        # get created_by user
        user = self.context["request"].user
        validated_data["created_by"] = user
        paragraphs_data = validated_data.pop("paragraphs")
        report = models.Report.objects.create(**validated_data)
        for paragraph_data in paragraphs_data:
            # add created_by user to paragraph data
            paragraph_data["created_by"] = user
            paragraph = models.Paragraph.objects.create(**paragraph_data)
            report.paragraphs.add(paragraph)
        return report
