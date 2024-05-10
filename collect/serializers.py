from rest_framework import serializers


class CreateSummarizeUrlsSerializer(serializers.Serializer):
    """Serializer for summarizing URLs"""

    urls = serializers.ListField(child=serializers.CharField(), required=True)
