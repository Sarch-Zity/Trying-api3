from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .serializers import CustomUserSerializer, UpdateCustomUserSerializer
from .models import CustomUser

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import IsAuthenticated

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
    user.email = user.email.lower()
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
            return Response(None, status=409)
        return Response(data.errors, status=400)

@api_view(["POST"])
def signin(request):
    login = request.data.get("login")
    password = request.data.get("password")
    user = authenticate(login = login, password = password)
    if user is not None:
        token = RefreshToken.for_user(user)
        return Response({"token": str(token.access_token)})
    else:
        return Response(None, 401)

@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def me(request):
    if request.method == "GET":
        print(request.data)
        data = request.user
        output = getuser(data)
        print(output)
        return Response(output, status=200)
    else:
        data = UpdateCustomUserSerializer(request.user, data = request.data, partial = True)
        if data.is_valid():
            if request.data.get("phone") and CustomUser.objects.filter(phone = data.validated_data["phone"]).exists():
                return Response(None, 409)
            data.save()
            output = getuser(CustomUser.objects.get(login = request.user.login))
            return Response(output, status=200)
        else:
            return Response(data.errors, status=400)
            
            