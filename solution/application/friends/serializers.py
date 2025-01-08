from rest_framework import serializers
from .models import Friend
from django.core.validators import MinValueValidator, MaxValueValidator

class FriendsSerializer(serializers.ModelSerializer):
    login = serializers.CharField(source="friend.login")
    addedAt = serializers.DateTimeField(source="date", format="%Y-%m-%dT%H:%M:%SZ")
    
    class Meta:
        model = Friend
        fields = ["login", "addedAt"]

class PaginatorSerializer(serializers.Serializer):
    offset = serializers.IntegerField(default=0, validators=[MinValueValidator(0)])
    limit = serializers.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(50)])