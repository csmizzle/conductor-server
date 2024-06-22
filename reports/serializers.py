"""
Report and paragraph serializers
"""
from rest_framework import serializers
from reports import models
from agents.serializers import CrewRunSerializer


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


class ParsedReportSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True)

    class Meta:
        model = models.ParsedReport
        fields = ["id", "title", "description", "sections"]

    def create(self, validated_data) -> models.ParsedReport:
        user = self.context["request"].user
        sections_data = validated_data.pop("sections")
        parsed_report = models.ParsedReport.objects.create(**validated_data)
        for section_entry in sections_data:
            paragraphs_data = section_entry.pop("paragraphs")
            section_entry["created_by"] = user
            section = models.Section.objects.create(**section_entry)
            for paragraph_entry in paragraphs_data:
                paragraph_entry["created_by"] = user
                paragraph = models.Paragraph.objects.create(**paragraph_entry)
                section.paragraphs.add(paragraph)
            parsed_report.sections.add(section)
        return parsed_report


class ReportSerializer(serializers.ModelSerializer):
    report = ParsedReportSerializer()
    crew_run = CrewRunSerializer()

    class Meta:
        model = models.Report
        fields = ["id", "report", "crew_run", "raw", "style"]

    def create(self, validated_data) -> models.Report:
        # get created_by user
        user = self.context["request"].user
        validated_data["created_by"] = user
        # create parsed report
        parsed_report_data = validated_data.pop("report")
        # add created by user to parsed report
        parsed_report_data["created_by"] = user
        sections_data = parsed_report_data.pop("sections")
        parsed_report = models.ParsedReport.objects.create(**parsed_report_data)
        # create sections and paragraphs
        for section_entry in sections_data:
            paragraphs_data = section_entry.pop("paragraphs")
            section_entry["created_by"] = user
            section = models.Section.objects.create(**section_entry)
            for paragraph_entry in paragraphs_data:
                paragraph_entry["created_by"] = user
                paragraph = models.Paragraph.objects.create(**paragraph_entry)
                section.paragraphs.add(paragraph)
            parsed_report.sections.add(section)
        # place parsed report in validated data
        validated_data["report"] = parsed_report
        report = models.Report.objects.create(**validated_data)
        return report
