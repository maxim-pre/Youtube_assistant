from rest_framework import serializers

class YoutubeAssistantDataSerializer(serializers.Serializer):
    url = serializers.CharField()
    query = serializers.CharField()