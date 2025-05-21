from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.

def alphanumeric(value):
    if not str(value).isalnum():
        raise ValidationError("only alphabels and numbers are allowed")
    return value


class Showroomlist(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    website = models.URLField(max_length=200)



    def __str__(self):
        return self.name
class Carlist(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    chassinumber = models.CharField(max_length=50,blank=True,null=True,validators=[alphanumeric])
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    showroom = models.ForeignKey(Showroomlist, on_delete=models.CASCADE,related_name='showrooms',null=True,blank=True)
    # showrooms = models.ManyToManyField(Showroomlist,related_name='showrooms',null=True,blank=True)


    def __str__(self):
        return self.name
    

class Review(models.Model):
    rating = models.IntegerField(validators=[MaxValueValidator,MinValueValidator])
    comment = models.CharField(max_length=200,null=True) 
    car = models.ForeignKey(Carlist,on_delete=models.CASCADE,related_name="reviews",null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "The rating of " + self.car.name + ":----" + str(self.rating)