from django.forms import ModelForm,EmailField,PasswordInput,CharField
from .models import Purchaser
class UserRegisterForm(ModelForm):
    email=EmailField()
    password=CharField(widget=PasswordInput())

    class Meta:
        model=Purchaser
        fields=['name','email','password','address','phone_number']
