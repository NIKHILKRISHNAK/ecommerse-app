from django.shortcuts import render
from seller.models import Items
def landing(request):
    items=Items.objects.all()
    return render(request,'landing.html',{'items':items})