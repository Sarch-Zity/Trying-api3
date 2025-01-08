from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Post
from users.models import CustomUser
from friends.models import Friend
from .serializers import CreatePostSerializer, PostSerializer

from friends.serializers import PaginatorSerializer

# Create your views here.
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def new(request):
    request.data["author"] = request.user.id
    serializer = CreatePostSerializer(data = request.data)
    if serializer.is_valid():
        post = serializer.save()
        post = PostSerializer(post)
        return Response(post.data, status=200)
    else:
        return Response(serializer.errors, status=400)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getbyid(request, id):
    try:
        post = Post.objects.get(id = id)
    except:
        return Response({"error": "Указанный пост не найден."}, status=404)
    if not post.author.isPublic and request.user != post.author:
        friendship = Friend.objects.filter(friendsowner = post.author).filter(friend = request.user).exists()
        if not friendship:
            return Response({"error": "Нет доступа к посту."}, status=404)
    serializer = PostSerializer(post)
    return Response(serializer.data, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def feed(request, login):
    if login == "my":
        login = request.user.login
    try:
        user = CustomUser.objects.get(login = login)
    except:
        return Response({"error": "Пользователь не найден"}, status=404)
    if not user.isPublic and user != request.user:
        friendship = Friend.objects.filter(friendsowner = user).filter(friend = request.user).exists()
        if not friendship:
            return Response({"error": "Нет доступа"}, status=404)
    paginator = PaginatorSerializer(data = request.GET)
    if not paginator.is_valid():
        return Response(paginator.errors, status=400)
    offset = paginator.validated_data["offset"]
    limit = paginator.validated_data["limit"]
    posts = Post.objects.filter(author = user.id).order_by("-createdAt")[offset:offset + limit]
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=200)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like(request, id):
    try:
        post = Post.objects.get(id = id)
    except:
        return Response({"error": "Указанный пост не найден."}, status=404)
    if not post.author.isPublic and request.user != post.author:
        friendship = Friend.objects.filter(friendsowner = post.author).filter(friend = request.user).exists()
        if not friendship:
            return Response({"error": "Нет доступа к посту."}, status=404)
    post.dislikesCount.remove(request.user)    
    post.likesCount.add(request.user)
    post.save()
    serializer = PostSerializer(post)
    return Response(serializer.data, status=200)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def dislike(request, id):
    try:
        post = Post.objects.get(id = id)
    except:
        return Response({"error": "Указанный пост не найден."}, status=404)
    if not post.author.isPublic and request.user != post.author:
        friendship = Friend.objects.filter(friendsowner = post.author).filter(friend = request.user).exists()
        if not friendship:
            return Response({"error": "Нет доступа к посту."}, status=404)
    post.likesCount.remove(request.user)
    post.dislikesCount.add(request.user)    
    post.save()
    serializer = PostSerializer(post)
    return Response(serializer.data, status=200)