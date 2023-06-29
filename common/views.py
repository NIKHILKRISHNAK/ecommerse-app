from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import AuthenticationForm

def login_user(request):
    if request.POST:
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            login(request,user)
            if user.is_staff:
                return redirect('/seller/')
            else:
                return redirect('/')
        else:
            form=AuthenticationForm(request,request.POST)
            return render(request,'common/login.html',{'form':form})
    form=AuthenticationForm()
    return render(request,'common/login.html',{'form':form})
# Create your views here.
