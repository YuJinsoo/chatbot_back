from django.urls import path
from .views import ChatbotView, ChatBotAnswer, hello_rest_api

app_name="chatbot"

urlpatterns = [
	path('', ChatbotView.as_view(), name='chat'),
	path('answer/', ChatBotAnswer.as_view(), name='answer'),
	path('test/', hello_rest_api, name='test'),
]