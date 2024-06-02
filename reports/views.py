from rest_framework import viewsets, permissions
from reports import models
from reports import serializers


class ParagraphViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows paragraphs to be viewed or edited.
    """

    serializer_class = serializers.ParagraphSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Paragraph.objects.filter(created_by=self.request.user)


class ReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reports to be viewed or edited.
    """

    serializer_class = serializers.ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Paragraph.objects.filter(created_by=self.request.user)
