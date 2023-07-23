from django.urls import path 
from .views import AiResponse

urlpatterns = [
    path('youtube_assistant/', AiResponse, name='youtube-assistant')
]