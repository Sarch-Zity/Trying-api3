from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Friend
from users.models import CustomUser
from .serializers import FriendsSerializer, PaginatorSerializer

# Create your views here.
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add(request):
    try:
        friend = CustomUser.objects.get(login = request.data.get("login"))
    except:
        return Response({"error": "Пользователь с указанным логином не найден."}, status=404)
    if friend == request.user: return Response({"status": "ok"}, status=200)
    friendship = Friend.objects.filter(friendsowner = request.user).filter(friend = friend).exists()
    if friendship:
        return Response({"status": "ok"}, status=200)
    data = Friend(friendsowner = request.user, friend =  friend)
    data.save()
    return Response({"status": "ok"}, status=200)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def remove(request):
    try:
        friend = CustomUser.objects.get(login = request.data.get("login"))
    except:
        return Response({"status": "ok"}, status=200)
    friendship = Friend.objects.filter(friendsowner = request.user).filter(friend = friend)
    if friendship.exists():
        friendship.delete()
    return Response({"status": "ok"}, status=200)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def friendslist(request):
    friends = Friend.objects.filter(friendsowner = request.user.id).order_by("-date")
    paginator = PaginatorSerializer(data = request.GET)
    if not paginator.is_valid():
        return Response(paginator.errors, status=400)
    offset = paginator._validated_data["offset"]
    limit = paginator._validated_data["limit"]
    result = FriendsSerializer(friends[offset:offset+limit], many=True)
    return Response(result.data)

# def friendslist(request):
#     paginator = LimitOffsetPagination()
#     paginator.max_limit = 50
#     limit = request.data.get("limit")
#     offset = request.data.get("limit")
#     if limit:
#         paginator.default_limit = limit
#     else:
#         paginator.default_limit = 5
#     friends = Friend.objects.filter(friendsowner = request.user.id).order_by("date").reverse()
#     result = paginator.paginate_queryset(friends, request)
#     result = FriendsSerializer(result, many=True)
#     return paginator.get_paginated_response(result.data)