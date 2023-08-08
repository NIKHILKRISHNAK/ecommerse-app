from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import ChangeDeliveryStatusForm
import json
from django.core import serializers 
# Create your views here.

@staff_member_required
def landing(request):
    items=Items.objects.filter(added_by=request.user)
    orders=Orders.objects.filter(item__added_by=request.user)
    ItemsName=[]
    ItemsNumber=[]
    OrdersName=[]
    for item in items:
        ItemsName.append(item.name)
        ItemsNumber.append(item.count)
    for order in orders:
        OrdersName.append(order.item.name)
    
    context={
        'ItemsName':ItemsName,
        'ItemsNumber':ItemsNumber,
        'OrdersName':OrdersName
    }
    JsonData=json.dumps(context)
    return render(request,'seller/landing.html',{'items':items,'orders':orders,'JsonData':JsonData})
@staff_member_required
def items(request):
    items=Items.objects.all()
    return render(request,'seller/items.html',{'items':items})

@staff_member_required
def details(request,id):
    item=Items.objects.get(id=id)
    print(item.count)
    if (item.count)==0:
        no="zero"
        return render(request,'seller/details.html',{'item':item,'no':no})
    return render(request,'seller/details.html',{'item':item})

@staff_member_required
def create_item(request):
    category_list=['Bags','Laptops','Mobile Phones','Kids','Electronics','School & Accessories','MakeUp','Outit']
    if request.method == 'POST':
        name=request.POST['name']
        description=request.POST['description']
        image=request.FILES['image']
        price=request.POST['price']
        category=request.POST['category']
        count=request.POST['count']
        added_by=request.POST['added_by']
        form=Items(name=name,description=description,image=image,price=price,category=category,count=count,added_by=added_by)

        print("form taken")
        print("form validated")
        form.save()
        print("Saved")
        return redirect('/seller/items/')
    return render(request,'seller/createitem.html',{'category_list':category_list})

@staff_member_required
def update(request,id):
    category_list=['Bags','Laptops','Mobile Phones','Kids','Electronics','School & Accessories','MakeUp','Outit']
    item=Items.objects.get(id=id)
    if request.POST:
        #name=request.POST['name']
        #description=request.POST['description']
        #image=request.FILES['image']
        #price=request.POST['price']
        #category=request.POST['category']
        #count=request.POST['count']
        #added_by=request.POST['added_by']
        #form=Items(name=name,description=description,image=image,price=price,category=category,count=count,added_by=added_by)
        form=CreateItemForm(request.POST,request.FILES,instance=item)

        print('form added')
        #if form.is_valid():
        print('validated')
        form.save()
        return redirect(f'/seller/details/{id}')
    form=CreateItemForm(instance=item)
    return render(request,'seller/update.html',{'form':form,'item':item,'category_list':category_list})

@staff_member_required
def delete(request,id):
    item=Items.objects.get(id=id)
    item.delete()
    return redirect('/seller/items/')

@staff_member_required
def create_seller(request):
    if request.POST:
        print('request recieved')
        form=UserCreationForm(request.POST or None)
        print('form taken')
        if form.is_valid():
            print('validated')
            User=form.save(commit=False)
            User.is_staff=True
            User.save()
            print('new seller created')
            return redirect('/login/')
    form=UserCreationForm()
    return render(request,'seller/create_seller.html',{'form':form})

@staff_member_required
def get_orders(request):
    orders=Orders.objects.filter(item_adder=request.user)
    print(len(orders))
    if len(orders)==0:
        message="No Orders"
        return render(request,'seller/orders.html',{'orders':orders,'message':message})

    print(orders)
    return render(request,'seller/orders.html',{'orders':orders})

@login_required
@staff_member_required
def order_details(request,id):
    order=Orders.objects.get(id=id)
    if request.POST:
        form=ChangeDeliveryStatusForm(request.POST,instance=order)
        print('form taken')
        if form.is_valid():
            print('validated')
            form.save()
            print('Updated')
            status=form.cleaned_data['order_status']
            print(status)
            if status=='Cancelled':
                order.delete()
            return redirect('/seller/orders/')
        else:
            print(form.errors)
    form=ChangeDeliveryStatusForm(instance=order)
    return render(request,'seller/orderdetails.html',{'order':order,'form':form})

def remove_from_order(request,id):
    order=Orders.objects.get(id=id)
    return redirect('seller/orderdetails.html')