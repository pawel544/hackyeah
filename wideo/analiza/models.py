from django.db import models

# Create your models here.
class Movies(models.Model):
    movies=models.CharField(max_length=35,null=False, unique=False)
    def __str__(self):
        return f"{self.movies}"

class Start(models.Model):
    start= models.CharField(max_length=10,null=False, unique=False)
    number_start= models.IntegerField()
    def __str__(self):
        return f"{self.start} - {self.number_start}"

class End(models.Model):
    end= models.CharField(max_length=10,null=False, unique=False)
    end= models.IntegerField()
    def __str__(self):
        return f"{self.end} - {self.end}"