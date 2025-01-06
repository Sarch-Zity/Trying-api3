from django.db import models

# Create your models here.

class Countries(models.Model):
    name = models.CharField()
    alpha2 = models.CharField(max_length=2)
    alpha3 = models.CharField(max_length=3)
    region = models.CharField(blank=True)

    class Meta:
        db_table = "countries"
        managed = False
