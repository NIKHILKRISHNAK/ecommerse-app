from django.forms import ModelForm
from .models import Items
class CreateItemForm(ModelForm):
    class Meta:
        model=Items
        fields='__all__'