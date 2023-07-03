from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth.models import User
from seller.models import Items
from .models import *

def UserRegister(request):
    if request.POST:
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            account=User.objects.create_user(user.name,form.cleaned_data['email'],form.cleaned_data['password'])
            account.save()
            user.account=account
            user.save()
            form.save()
            return redirect('/login/')
    form=UserRegisterForm()
    return render(request,'user/userregister.html',{'form':form})

def details(request,id):
    item=Items.objects.get(id=id)
    print('inside item:',item)
    items=item.name
    print(items)
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

def delete_from_cart(request,id):
    carts=Cart.objects.filter(name=request.user)
    print('worked')
    item_to_delete=Cart.objects.filter(name=request.user,id=id)
    print(item_to_delete)
    item_to_delete.delete()
    print('deleted from cart')
    if len(carts)==0:
        empty="Your cart is empty"
        return render(request,'user/cart.html',{'carts':carts,'empty':empty})
    return render(request,'user/cart.html',{'carts':carts})

def change_details(request,id):
    user_profile=Purchaser.objects.get(account_id=request.user.id)
    if request.POST:
        form=EditAddressAndPhoneNo(request.POST,instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect(f'/user/buynow/2/{id}')
    form=EditAddressAndPhoneNo(instance=user_profile)
    item=Items.objects.get(id=id)
    return render(request,'user/changedetails.html',{'form':form,'item':item})

def buy_now(request,id):
    item=Items.objects.get(id=id)
    return render(request,'user/buynow.html',{'item':item})

def place_order(request,id):
    items=Items.objects.get(id=id)
    cart=Cart.objects.get(name=request.user,item=items.name)
    print(cart.item)

    print(items.count)
    if request.POST:
        Count=request.POST.get('number')
        print(Count)
        items.count-=int(Count)
        items.save()
        cart.delete()
        print('deleted after place order')
        return redirect('/user/thankyou/')
    return render(request,'user/confirmorder.html',{'items':items})

def thankyou(request):
    return render(request,'user/thankyou.html')

def cart_to_details(request,name):
    item=Items.objects.get(name=name)
    print(item)
    items=item.name
    print(items)
    try:
        check=Cart.objects.get(item=items,name=request.user)
        message="Item is already added to the Cart"
        return render(request,'user/details.html',{'item':item,'message':message})
    except:
        if request.POST:
            cart=Cart(name=request.user,item=items)
            cart.save()
    return render(request,'user/details.html',{'item':item})
