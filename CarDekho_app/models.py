from django.db import models

# Create your models here.
class Carlist(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    chassinumber = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)

    

    