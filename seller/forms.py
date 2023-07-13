from django.forms import ModelForm
from .models import Items
from django import forms
category_list=['Bags','Laptops','Mobile Phones','Kids','Electronics','School & Accessories','MakeUp','Outit']

class CreateItemForm(ModelForm):
    class Meta:
        model=Items
        fields='__all__'
    def __init__(self,*args,**kwargs):
        super(CreateItemForm,self).__init__(*args,**kwargs)
        self.fields['added_by'].widget.attrs['readonly']=True
        self.fields['category'].widget=forms.Select(choices=[
            ('Bags','Bags'),
            ('Laptops','Laptops'),
            ('Mobile Phones','Mobile Phones'),
            ('Kids','Kids'),
            ('Electronics','Electronics'),
            ('School & Accessories','School & Accessories'),
            ('MakUp','MakUp'),
            ('Outfit','Outfit')
            ])