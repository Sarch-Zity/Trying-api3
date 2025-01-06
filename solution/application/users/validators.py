from django.core.exceptions import ValidationError
import re
from countries.models import Countries

def passwordvalidator(value):
    if not re.search(r'[a-z]', value):
        raise ValidationError("Нет нижнего регистра")
    if not re.search(r'[A-Z]', value):
        raise ValidationError("Нет верхнего регистра")
    if not re.search(r'[0-9]', value):
        raise ValidationError("Пароль должен содержать хотя бы одну циру")
    
def countrycodevalidator(value):
    if not Countries.objects.filter(alpha2 = value.upper()).exists():
        raise ValidationError("Не найдена указаная страна")