from django import forms

class contactForm(forms.Form):
    name = forms.CharField(required=False, max_length=100, help_text='Your Name Here (max 100 chars))')
    email = forms.EmailField(required=True)
    comment = forms.CharField(required=True, widget=forms.Textarea)
