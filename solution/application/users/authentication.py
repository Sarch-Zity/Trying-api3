from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import BlacklistedAccessToken
from rest_framework_simplejwt.exceptions import InvalidToken

class CustomJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        validated_token = super().get_validated_token(raw_token)
        jti = validated_token.get('jti')
        if BlacklistedAccessToken.objects.filter(jti=jti).exists():
            raise InvalidToken("Этот токен был отозван.")
        return validated_token