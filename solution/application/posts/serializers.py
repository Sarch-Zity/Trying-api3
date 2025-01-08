from rest_framework import serializers
from .models import Post

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["author", "content", "tags"]

class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.login")
    createdAt = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    likesCount = serializers.SerializerMethodField()
    dislikesCount = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "author", "content", "tags", "createdAt", "likesCount", "dislikesCount"]
    
    def get_likesCount(self, obj):
        return obj.likesCount.count()
    
    def get_dislikesCount(self, obj):
        return obj.dislikesCount.count()