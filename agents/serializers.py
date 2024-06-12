from rest_framework import serializers


class URLMarketingCrewSerializer(serializers.Serializer):
    url = serializers.CharField()
