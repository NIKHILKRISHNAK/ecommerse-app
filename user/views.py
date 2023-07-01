from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth.models import User
from seller.models import Items
from .models import *

def UserRegister(request):
    if request.POST:
        form=UserRegisterForm(request.POST)
        print("got request")
        if form.is_valid():
            print("validated")
            user=form.save(commit=False)
            print("form.save(commit)")
            account=User.objects.create_user(user.name,form.cleaned_data['email'],form.cleaned_data['password'])
            print("account all")
            account.save()
            print("account.save")
            user.account=account
            print("user.account=account")
            user.save()
            print("user.save")
            form.save()
            print("saved")
            print(form.errors)
            return redirect('/login/')
    form=UserRegisterForm()
    return render(request,'user/userregister.html',{'form':form})

def details(request,id):
    item=Items.objects.get(id=id)
    items=item.name
    try:
        check=Cart.objects.get(item=items,name=request.user)
        message="Item is already added to the Cart"
        return render(request,'user/details.html',{'item':item,'message':message})
    except:
        if request.POST:
            cart=Cart(name=request.user,item=items)
            cart.save()
    return render(request,'user/details.html',{'item':item})

def show_cart(request):
    carts=Cart.objects.filter(name=request.user)
    if len(carts)==0:
        empty="Your cart is empty"
        return render(request,'user/cart.html',{'carts':carts,'empty':empty})
    return render(request,'user/cart.html',{'carts':carts})

def buy_now(request,id):
    items=Items.objects.get(id=id)
    return render(request,'user/buynow1.html',{'items':items})

def change_details(request,id):
    return render(request,'user/changedetails.html')