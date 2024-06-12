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


class Report(models.Model):
    task = models.ForeignKey(
        ChainTask, on_delete=models.CASCADE, related_name="report", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    paragraphs = models.ManyToManyField(Paragraph, related_name="paragraphs")

    def __str__(self):
        return self.title

    def to_pydantic(self) -> pydantic_models.Report:
        paragraphs = [paragraph.to_pydantic() for paragraph in self.paragraphs.all()]
        return pydantic_models.Report(
            title=self.title,
            description=self.description,
            paragraphs=paragraphs,
        )
