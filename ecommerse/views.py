from django.shortcuts import render
from seller.models import Items
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from user.models import Purchaser
def landing(request):
    items=Items.objects.all()
    return render(request,'landing.html',{'items':items})
@login_required
def profile(request):
    user=User.objects.get(username=request.user)
    print(user.date_joined)
    print(user.email)
    email=user.email
    date=user.date_joined
    if request.user.is_staff:
        print("staff")
        items=Items.objects.filter(added_by=request.user)
        if len(items)==0:
            return render(request,'profile.html',{'date':date,'email':email,'items':items,'message':'Error'})
        return render(request,'profile.html',{'date':date,'email':email,'items':items,})
    elif not request.user.is_superuser and not request.user.is_staff and request.user.is_active:
        purchaser=Purchaser.objects.get(name=request.user)
        return render(request,'profile.html',{'date':date,'email':email,'user':purchaser})
    return render(request,'profile.html')