from django.db import models

# Create your models here.
class UpdateInfo(models.Model):
    University_Name = models.CharField(max_length=200,blank=True,null=True)
    Country_Name = models.CharField(max_length=200,blank=True,null=True)
    CodeForces_Handle = models.CharField(max_length=200,blank=True,null=True)
    Toph_Handle = models.CharField(max_length=200,blank=True,null=True)
    