from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .serializers import CustomUserSerializer, UpdateCustomUserSerializer, UpdatePasswordCustomUserSerializer
from .models import CustomUser, AccessTokenList, BlacklistedAccessToken

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from uuid import uuid4

from rest_framework.permissions import IsAuthenticated

from friends.models import Friend

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def test(request):
    
    return Response({"1": "1"})

def closeaccess(user):
    token = AccessTokenList.objects.filter(user = user)
    if token.exists():
        token = token.first()
        BlacklistedAccessToken.objects.create(jti = token.jti)
        token.delete()

def isnewuser(data):
    login = not CustomUser.objects.filter(login = data.data.get("login")).exists()
    email = not CustomUser.objects.filter(email = data.data.get("email")).exists()
    if data.data.get("phone"):
        phone = not CustomUser.objects.filter(phone = data.data.get("phone")).exists()
    else:
        phone = True
    
    if all([login, email, phone]):
        return True
    else:
        return False
    
def createuser(fields):
    user = CustomUser(**fields)
    # user.email = user.email.lower()
    user.set_password(fields["password"])
    user.save()
    return user

def getuser(data):
    output = {
            'profile': {
                'login': data.login,
                'email': data.email,
                'countryCode': data.countryCode,
                'isPublic': data.isPublic,
                }
            }
    if data.phone:
            output['profile']['phone'] = data.phone
    if data.image:
        output['profile']['image'] = data.image
    
    return output

# # Create your views here.
@api_view(["POST"])
def register(request):
    data = CustomUserSerializer(data = request.data)
    if data.is_valid():
        if not isnewuser(request):
            return Response(None, status=409)
        data = createuser(data.validated_data)
        output = getuser(data)
        return Response(output, status=201)
    else:
        if not isnewuser(request):
            return Response({"error": "Нарушено требование на уникальность авторизационных данных пользователей."}, status=409)
        return Response(data.errors, status=400)

@api_view(["POST"])
def signin(request):
    login = request.data.get("login")
    password = request.data.get("password")
    user = authenticate(login = login, password = password)
    if user is not None:
        closeaccess(user)
        token = AccessToken.for_user(user)
        token['jti'] = str(uuid4())
        AccessTokenList.objects.create(jti = token['jti'], user = user)
        return Response({"token": str(token)})
    else:
        return Response({"error": "Пользователь с указанным логином и паролем не найден"}, 401)

@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def me(request):
    if request.method == "GET":
        data = request.user
        output = getuser(data)
        return Response(output['profile'], status=200)
    else:
        data = UpdateCustomUserSerializer(request.user, data = request.data, partial = True)
        if data.is_valid():
            if request.data.get("phone") and CustomUser.objects.filter(phone = data.validated_data["phone"]).exists() and request.user.phone != data.validated_data["phone"]:
                return Response({"error": "Нарушено требование на уникальность авторизационных данных пользователей."}, 409)
            data.save()
            output = getuser(CustomUser.objects.get(login = request.user.login))
            return Response(output['profile'], status=200)
        else:
            if not isnewuser(request):
                return Response({"error": "Нарушено требование на уникальность авторизационных данных пользователей."}, status=409)
            return Response(data.errors, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request, login):
    try:
        user = CustomUser.objects.get(login = login)
        friendship = Friend.objects.filter(friendsowner = user.id).filter(friend = request.user.id).exists()
        if user.isPublic or user == request.user or friendship:
            output = getuser(user)
            print(output)
            return Response(output['profile'], status=200)
        else:
            return Response({"error": "У отправителя запроса нет доступа к запрашиваемому профилю"}, status=403)
    except:
        return Response({"error": "Пользователь с указанным логином не существует"}, status=403)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def updatePassword(request):
    data = UpdatePasswordCustomUserSerializer(request.user, data = {"password": request.data.get("newPassword")}, partial = True)
    if request.user.check_password(request.data.get("oldPassword")):
        if data.is_valid():
            user = request.user
            user.set_password(data.validated_data["password"])
            user.save()
            closeaccess(request.user)
            return Response({"status": "ok"}, status=200)
        else:
            return Response(data.errors, status=400)
    else:
        return Response({"error": "Указанный пароль не совпадает с действительным."}, status=403)