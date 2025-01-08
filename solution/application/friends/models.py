from django.db import models
from users.models import CustomUser

# Create your models here.
class Friend(models.Model):
    friendsowner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="friendsowner")
    friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="friend")
    date = models.DateTimeField(auto_now_add=True)