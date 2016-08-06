from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

from .forms import contactForm

# Create your views here.

def contact(request):
    form = contactForm(request.POST or None)
    title = 'Contact'
    confirm_message = None

    if form.is_valid():
        #print(form.cleaned_data['email'])
        comment = form.cleaned_data['comment']
        name = form.cleaned_data['name']
        from_email = form.cleaned_data['email']
        subject = 'Message from guest[%s] comment' % from_email
        message = 'From [%s]: %s' % (name, comment)
        to_email = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_email, fail_silently=False)
        title = 'Thanks'
        confirm_message = "Thanks for the submission"
        form = None
        
    context = {'title': title, 'form': form, 'confirm_message': confirm_message}
    template = 'contact.html'
    return render(request, template, context)
