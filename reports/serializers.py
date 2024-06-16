"""
Report and paragraph serializers
"""
from rest_framework import serializers
from reports import models


class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Paragraph
        fields = ["id", "title", "content"]

    def create(self, validated_data) -> models.Paragraph:
        user = self.context["request"].user
        validated_data["created_by"] = user
        paragraph = models.Paragraph.objects.create(**validated_data)
        return paragraph


class SectionSerializer(serializers.ModelSerializer):
    paragraphs = ParagraphSerializer(many=True)

    class Meta:
        model = models.Section
        fields = ["id", "title", "paragraphs"]

    def create(self, validated_data) -> models.Section:
        user = self.context["request"].user
        validated_data["created_by"] = user
        section = models.Section.objects.create(**validated_data)
        return section


class ReportSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True)

    class Meta:
        model = models.Report
        fields = ["id", "title", "description", "sections"]

    def create(self, validated_data) -> models.Report:
        # get created_by user
        user = self.context["request"].user
        validated_data["created_by"] = user
        sections_data = validated_data.pop("sections")
        report = models.Report.objects.create(**validated_data)
        for section_entry in sections_data:
            paragraphs_data = section_entry.pop("paragraphs")
            section_entry["created_by"] = user
            section = models.Section.objects.create(**section_entry)
            for paragraph_entry in paragraphs_data:
                paragraph_entry["created_by"] = user
                paragraph = models.Paragraph.objects.create(**paragraph_entry)
                section.paragraphs.add(paragraph)
            report.sections.add(section)
        return report
