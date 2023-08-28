from django.urls import path
from .views import ChatbotView, ChatBotAnswer, CreateChatRoom, DetailChatRoom, DeleteChatRoom, hello_rest_api

app_name="chatbot"

urlpatterns = [
	path('', ChatbotView.as_view(), name='chat'),
	path('answer/', ChatBotAnswer.as_view(), name='answer'),
	path('create/room/', CreateChatRoom.as_view(), name='create-room'),
	path('detail/room/<int:roomId>/', DetailChatRoom.as_view(), name='detail-room'),
	path('create/room/<int:roomId>/', DeleteChatRoom.as_view(), name='delete-room'),
 
	path('test/', hello_rest_api, name='test'),
]