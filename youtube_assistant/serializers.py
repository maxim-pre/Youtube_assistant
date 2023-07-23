from rest_framework import serializers
from lib.functions import is_valid_youtube_url


class YoutubeAssistantDataSerializer(serializers.Serializer):
    url = serializers.CharField(validators=[is_valid_youtube_url])
    query = serializers.CharField()