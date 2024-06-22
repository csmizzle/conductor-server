from django.db import models
from django.contrib.auth.models import User
from conductor.reports import models as pydantic_models
from chains.models import ChainTask


# Create your models here.
class Paragraph(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title

    def to_pydantic(self) -> pydantic_models.Paragraph:
        return pydantic_models.Paragraph(
            title=self.title,
            content=self.content,
        )


class Section(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    paragraphs = models.ManyToManyField(Paragraph, related_name="paragraphs")

    def __str__(self):
        return self.title

    def to_pydantic(self) -> pydantic_models.Section:
        paragraphs = [paragraph.to_pydantic() for paragraph in self.paragraphs.all()]
        return pydantic_models.Section(
            title=self.title,
            paragraphs=paragraphs,
        )


class ParsedReport(models.Model):
    task = models.ForeignKey(
        ChainTask, on_delete=models.CASCADE, related_name="report", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    sections = models.ManyToManyField(Section, related_name="sections")

    def __str__(self):
        return self.title

    def to_pydantic(self) -> pydantic_models.Report:
        sections = [section.to_pydantic() for section in self.sections.all()]
        return pydantic_models.ParsedReport(
            title=self.title,
            description=self.description,
            sections=sections,
        )


class Report(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.ForeignKey(
        ParsedReport, on_delete=models.CASCADE, null=True, related_name="report"
    )
    raw = models.TextField(null=True, blank=True)
    style = models.CharField(
        max_length=255,
        choices=[(tag.name, tag.value) for tag in pydantic_models.ReportStyle],
        default=pydantic_models.ReportStyle.BULLETED.value,
    )

    def __str__(self):
        return self.raw

    def to_pydantic(self) -> pydantic_models.Report:
        return pydantic_models.Report(
            report=self.report.to_pydantic(),
            raw=self.raw,
            style=pydantic_models.ReportStyle(self.style),
        )
