import sys
from django.shortcuts import render
from .serializers import YoutubeAssistantDataSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from lib.chatgpt import *

# Create your views here.

@api_view(['POST'])
def AiResponse(request):
    serializer = YoutubeAssistantDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    try:
        db = create_db_from_youtube_video_url(validated_data['url'])
        return Response({
            "response": get_response_from_query(db, validated_data['query'])
        })
    except:
        return Response('something went wrong. Please try using a different Youtube URL')




