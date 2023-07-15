from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your views here.

@staff_member_required
def landing(request):
    return render(request,'seller/landing.html')
@staff_member_required
def items(request):
    items=Items.objects.all()
    return render(request,'seller/items.html',{'items':items})

@staff_member_required
def details(request,id):
    item=Items.objects.get(id=id)
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
    orders=Orders.objects.all()
    print(orders)
    return render(request,'seller/orders.html',{'orders':orders})