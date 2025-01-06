from rest_framework import serializers
from .models import Countries

class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = ["name", "alpha2", "alpha3", "region"]