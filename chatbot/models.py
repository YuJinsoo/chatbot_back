from django.db import models
from django.contrib.auth import get_user_model

account = get_user_model()

class Conversation(models.Model):
    chatroom = models.ForeignKey('ChatRoom', on_delete=models.CASCADE)
    prompt = models.CharField(max_length=512)
    response = models.TextField()

    def __str__(self):
        return f"{self.prompt}: {self.response}"


class ChatRoom(models.Model):
    creator = models.ForeignKey(account, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)