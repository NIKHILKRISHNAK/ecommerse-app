from django.db import models
from user.models import Purchaser
from datetime import datetime
# Create your models here.
class Items(models.Model):
    name=models.CharField(max_length=30)
    description=models.TextField()
    image=models.ImageField(upload_to='uploads/')
    price=models.DecimalField(max_digits=10, decimal_places=2)
    category=models.CharField(max_length=30)
    count=models.IntegerField(default=1)
    added_by=models.CharField(max_length=30,default=None)
    def __str__(self):
        return self.name
    
class Orders(models.Model):
    item=models.ForeignKey(Items,on_delete=models.CASCADE)
    ordered_by=models.ForeignKey(Purchaser,on_delete=models.CASCADE)
    date=models.DateField(default=datetime.now)
    def __str__(self):
        return self.item.name