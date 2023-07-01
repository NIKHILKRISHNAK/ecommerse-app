from django.db import models
from django.contrib.auth.models import User

    
class Purchaser(models.Model):
    account=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=150)
    address=models.TextField()
    phone_number=models.CharField(max_length=13)
    def __str__(self):
        return self.name
# Create your models here.

class Cart(models.Model):
   # name=models.ForeignKey(Purchaser,on_delete=models.CASCADE)
    name=models.CharField(max_length=150)
    item=models.CharField(max_length=150,default=None)
    def __str__(self):
        return self.item