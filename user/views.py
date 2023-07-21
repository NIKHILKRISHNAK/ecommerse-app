from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth.models import User
from seller.models import Items
from .models import *
from django.contrib.auth.decorators import login_required
import json
from seller.models import Orders
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
    count=item.count
    
    if count!=0:
        print(count)
        print('inside item:',item)
        items=item.name
        print(items)
        try:
            check=Cart.objects.get(item=items,name=request.user)
            message="Item is already added to the Cart"
            return render(request,'user/details.html',{'item':item,'already':message})
        except:
            if request.POST:
                if request.user.is_authenticated:
                    cart=Cart(name=request.user,item=items)
                    cart.save()
                else:
                    send='Please login to check your cart'
                    return render(request,'user/details.html',{'item':item,'send':send})
    else:
        message="Out of Stoke"
        return render(request,'user/details.html',{'item':item,'message':message})

    return render(request,'user/details.html',{'item':item})

@login_required
def show_cart(request):
    carts=Cart.objects.filter(name=request.user)
    if len(carts)==0:
        empty="Your cart is empty"
        return render(request,'user/cart.html',{'carts':carts,'empty':empty})
    return render(request,'user/cart.html',{'carts':carts})

@login_required
def remove_item_from_cart(request,id):
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
    item=Items.objects.get(id=id)
    if request.user.is_authenticated:
        if not request.user.is_superuser and not request.user.is_staff and request.user.is_active: 
            user_profile=Purchaser.objects.get(account_id=request.user.id)
            if request.POST:
                if request.user.is_authenticated:
                    form=EditAddressAndPhoneNo(request.POST,instance=user_profile)
                    if form.is_valid():
                        form.save()
                        return redirect(f'/user/buynow/2/{id}')
               
            form=EditAddressAndPhoneNo(instance=user_profile)
            item=Items.objects.get(id=id)
            return render(request,'user/changedetails.html',{'form':form,'item':item})
        else:
            return render(request,'user/changedetails.html',{'message':"You are not logged in  with a purchaser account",'item':item})

    else:
        message="Login required for next step"
        return render(request,'user/changedetails.html',{'message':message})

@login_required
def payment(request,id):
    total=0
    item=Items.objects.get(id=id)
    price=item.price
    context={
            'price':int(price)
        }
    json_data=json.dumps(context)
    if request.POST:
        choice=request.POST.get('payment_method')
        count=request.POST.get('number')
        print('count is ',count)
        print(item.count)
        if int(item.count) >= int(count):
            request.session['count']=count
            total=int(count)*(item.price)
            print(total)
            print(choice)
            if choice=='upi':
                request.session['payment']=choice
                return redirect(f'/user/upi/{id}')
            elif choice=='net_banking':
                request.session['payment']=choice
                return redirect(f'/user/net-banking/{id}')
            elif choice=='cash_on_delivery':
                request.session['payment']=choice
                return redirect(f'/user/buynow/3/{id}')
        else:
            return render(request,'user/payment.html',{'item':item,'total':total,'json_data':json_data,'message':"This much Items are not in the stoke"})
    return render(request,'user/payment.html',{'item':item,'total':total,'json_data':json_data})

def upi(request,id):
    return render(request,'user/upi.html')

def net_banking(request,id):
    return render(request,'user/net_banking.html')

def cash_on_delivery(request,id):
    return render(request,'user/cahs_on_delivery.html')

def place_order(request,id):
    if not request.user.is_superuser and not request.user.is_staff and request.user.is_active:
        user=Purchaser.objects.get(name=request.user)
        print(user)
        count=request.session.get('count')
        print('count in place order', count)
        items=Items.objects.get(id=id)
        total_amt=int(count)* int(items.price)

        def check():
            try:
                cart=Cart.objects.get(name=request.user,item=items.name)
                return True
            except:
                return False
                
        if request.POST:
            payment_method=request.session.get('payment')
            if items.count!= 0:
                print('first',items.count)
                items.count-=int(count)
                print('second',items.count)
                items.save()
                order=Orders()
                order.item=items
                order.ordered_by=user
                order.item_adder=items.added_by
                order.payment=payment_method
                order.save()
                if check():
                    Cart.objects.get(name=request.user,item=items.name).delete()
                    print('deleted after place order')    
                    return redirect('/user/thankyou/')
                return redirect('/user/thankyou/')
            else:
                message="Not available"
                return render(request,'user/confirmorder.html',{'items':items,'message':message})
        return render(request,'user/confirmorder.html',{'items':items,'total':total_amt,'user':user})
    return render(request,'user/confirmorder.html',{'items':items,'total':total_amt})

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
        return render(request,'user/details.html',{'item':item,'already':message})
    except:
        if request.POST:
            cart=Cart(name=request.user,item=items)
            cart.save()
    return render(request,'user/details.html',{'item':item})

@login_required
def orders(request):
    purchaser=Purchaser.objects.get(name=request.user)
    print(purchaser)
    user_orders=Orders.objects.filter(ordered_by=purchaser)
    print(user_orders)
    return render(request,'user/orders.html',{'orders':user_orders})

@login_required
def order_details(request,id):
    item=Orders.objects.get(id=id)
    print(item)
    return render(request,'user/orderdetails.html',{'item':item})