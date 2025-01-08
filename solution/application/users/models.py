from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator, MinLengthValidator
from .validators import passwordvalidator, countrycodevalidator

class CustomUserManager(BaseUserManager):
    def create_user(self, login, email, countryCode, isPublic, password=None, **extra_fields):
        if not email:
            raise ValueError('Email должен быть указан')
        email = self.normalize_email(email)
        user = self.model(login=login, email=email, countryCode = countryCode.upper(), isPublic = isPublic, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    login = models.CharField(max_length=30, unique=True, validators=[RegexValidator(r"^[a-zA-Z0-9-]+$")])
    email = models.EmailField(max_length=50, unique=True, validators=[MinLengthValidator(1)])
    password = models.CharField(max_length=100, validators=[MinLengthValidator(6), passwordvalidator])
    countryCode = models.CharField(max_length=2, validators=[RegexValidator(r"^[a-zA-Z]+$"), MinLengthValidator(2), countrycodevalidator])
    isPublic = models.BooleanField()
    phone = models.CharField(max_length=20, unique=True, null=True, validators=[RegexValidator(r"\+[\d]+")])
    image = models.URLField(max_length=200, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'login'  
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'countryCode', 'isPublic']

    def __str__(self):
        return self.login

class BlacklistedAccessToken(models.Model):
    jti = models.CharField(max_length=255, unique=True)

class AccessTokenList(models.Model):
    jti = models.CharField(max_length=255, unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True)