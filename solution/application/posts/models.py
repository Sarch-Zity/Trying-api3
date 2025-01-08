from django.db import models
import uuid
from users.models import CustomUser

# Create your models here.
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=1000)
    author = models.ForeignKey(CustomUser, related_name="author", on_delete=models.CASCADE)
    tags = models.JSONField()
    createdAt = models.DateTimeField(auto_now_add=True)
    likesCount = models.ManyToManyField(CustomUser, related_name="likesCount")
    dislikesCount = models.ManyToManyField(CustomUser, related_name="dislikesCount")