"""
Search endpoints serializers
"""
from rest_framework import serializers


class SearchInputSerializer(serializers.Serializer):
    """Serializer for search input"""
    query = serializers.CharField(max_length=255)


class SearchOutputSerializer(serializers.Serializer):
    """Serializer for search output"""
    results = serializers.ListField(child=serializers.CharField(max_length=255))
