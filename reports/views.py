from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework import status
from django.http.response import FileResponse
from reports import models
from reports import serializers
from conductor.reports.html_ import report_to_html
from pdfkit import from_string
import tempfile


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
        return models.Report.objects.filter(created_by=self.request.user)


class ReportToHtmlView(generics.RetrieveAPIView):
    """
    Convert a report to an HTML string
    """

    def get(self, request, report_id: int, *args, **kwargs):
        report = models.Report.objects.get(id=report_id)
        # Convert to pydantic model
        report_base = report.to_pydantic()
        html = report_to_html(report_base)
        return Response(html, status=status.HTTP_200_OK)


class ReportToPDFView(generics.RetrieveAPIView):
    """
    Convert a report to a PDF
    """

    def get(self, request, report_id: int, *args, **kwargs):
        report = models.Report.objects.get(id=report_id)
        # Convert to pydantic model
        report_base = report.to_pydantic()
        html = report_to_html(report_base)
        with tempfile.NamedTemporaryFile() as f:
            from_string(html, f.name)
            short_report = open(f.name, "rb")
            return FileResponse(short_report, as_attachment=True, filename="report.pdf")
