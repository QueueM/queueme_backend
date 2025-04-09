# chatApp/models.py
from django.db import models
from django.contrib.auth.models import User
from shopApp.models import ShopDetailsModel

class ChatRoomModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(ShopDetailsModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'shop')

    def __str__(self):
        return f"ChatRoom: User {self.user.username} - Shop {self.shop}"

class ChatHistoryModel(models.Model):
    room = models.ForeignKey(ChatRoomModel, on_delete=models.CASCADE)
    sent_by = models.IntegerField()  # e.g., 1 for user, 3 for bot/shop
    message = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.createdAt}] Sent by {self.sent_by}: {self.message[:50]}"
