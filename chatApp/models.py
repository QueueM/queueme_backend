from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from shopApp.models import ShopDetailsModel



class ChatRoomModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(ShopDetailsModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'shop')

class ChatHistoryModel(models.Model):
    room = models.ForeignKey(ChatRoomModel, on_delete=models.CASCADE)
    sent_by = models.IntegerField() # 1 for user 3 for shop
    message = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)