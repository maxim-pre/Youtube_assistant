import re
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

def is_valid_youtube_url(url):
    # Regular expression for matching YouTube URLs
    youtube_url_pattern = r'^https?://(?:www\.)?youtu(?:\.be/|be\.com/(?:watch\?v=|v/|embed/|user/))([\w-]{11})(?:\S+)?$'
    
    # Use re.match to check if the URL matches the pattern
    if not re.match(youtube_url_pattern, url):
        raise serializers.ValidationError("invalid Youtube Url")
