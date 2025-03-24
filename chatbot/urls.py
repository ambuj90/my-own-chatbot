from django.urls import path
from .views import chatbot_response, home

urlpatterns = [
    path('', home),
    path('chat/', chatbot_response, name='chatbot_response'),
]
