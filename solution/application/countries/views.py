from rest_framework.response import Response
from rest_framework.decorators import api_view
from countries.models import Countries
from .serializers import CountriesSerializer

# Create your views here.
@api_view(["GET"])
def countries(request):
    regions = dict(request.GET).get("region")
    countries = Countries.objects.all().order_by("alpha2")
    if regions:
        countries = countries.filter(region__in = regions)
    if not countries:
        return Response({"error": "Нет такой страны"}, 400)
    answer = CountriesSerializer(countries, many=True)
    return Response(answer.data)

@api_view(["GET"])
def countriesalpha(request, alpha2:str):
    try:
        country = Countries.objects.get(alpha2 = alpha2.upper())
    except:
        return Response({"error": "Нет такой страны"}, 400)
    answer = CountriesSerializer(country, many=False)

    return Response(answer.data)