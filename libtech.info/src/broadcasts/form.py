from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.utils.text import slugify

from .models import Broadcast

TO_CHOICES = (
    #('', ''),
    ('group', 'Group'),
    ('location', 'Location'),
    ('custom', 'Custom'),
)
    
class BroadcastModelForm(forms.ModelForm):
    to = forms.ChoiceField(choices=TO_CHOICES, required=False)
    description = forms.CharField(widget=forms.Textarea(
        attrs = {
            'class': 'custom-class',
            'placeholder': 'Description',
            'some-attr': 'this',
        }
    ))
    
    start_time = forms.DateTimeField(widget=AdminSplitDateTime())
    '''
        attrs = {
            'class': 'datetime',
        }))
    start_time = forms.DateTimeField(widget=forms.widgets.DateTimeInput(
        attrs={
            'class': 'date_picker',
            'placeholder': 'MUST FILL',
        }
    ))
    end_time = forms.DateTimeField(widget=AdminSplitDateTime)
    '''
    
    class Meta:
        model = Broadcast
        fields = [
            'name',
            'description',
            'media',
        ]
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'placeholder': 'Name of broadcast',
                }
            ),
            'description': forms.Textarea(
                attrs = {
                    'placeholder': 'Please write a description here',  # Failed to over ride the default in the model
                }
            ),
        }

    '''
    def clean(self):
        cleaned_data = super(BroadcastModelForm, self).clean()
        name = cleaned_data.get('name')
        slug = slugify(name)
        if Broadcast.objects.filter(slug=slug).exists():
            raise forms.ValidationError('Name is already taken. A new name is needed.')
        return cleaned_data
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 1.00 or price > 99.99:
            raise forms.ValidationError('Price should be < 100 and > 1')
        else:
            return price
    '''

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 3:
            return name
        else:
            raise forms.ValidationError('Name should be more than 3 chars long')
