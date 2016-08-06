from django import forms
from django.utils.text import slugify

from .models import Workdetail

class WorkdetailAddForm(forms.Form):
    title = forms.CharField(label='Overridden Label', widget=forms.TextInput(
        attrs = {
            'class': 'custom-class',
            'placeholder': 'Name',
        }
    ))
    
class WorkdetailModelForm(forms.ModelForm):
    class Meta:
        model = Workdetail
        fields = [
            'name',
        ]
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'placeholder': 'Enter Name Here',
                }
            ),
        }
    
