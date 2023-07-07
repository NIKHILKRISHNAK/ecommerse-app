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
    if request.method == 'POST':
        form=CreateItemForm(request.POST,request.FILES)
        print("form taken")
        if form.is_valid():
            print("form validated")
            form.save()
            print("Saved")
            return redirect('/seller/items/')
        else:
            print(form.errors)
    form=CreateItemForm()
    return render(request,'seller/createitem.html',{'form':form})

@staff_member_required
def update(request,id):
    item=Items.objects.get(id=id)
    if request.POST:
        form=CreateItemForm(request.POST,request.FILES,instance=item)
        if form.is_valid():
            form.save()
            return redirect(f'/seller/details/{id}')
    form=CreateItemForm(instance=item)
    return render(request,'seller/update.html',{'form':form,'item':item})

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
            User.is_superuser=True
            User.save()
            print('new seller created')
            return redirect('/login/')
    form=UserCreationForm()
    return render(request,'seller/create_seller.html',{'form':form})