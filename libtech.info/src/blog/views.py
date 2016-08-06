from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect

from .models import Blog
from .forms import BlogForm

# Create your views here.

def blog_create(request):
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404

    form = BlogForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Successfully Created')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'form': form,
    }
    return render(request, 'blog_form.html', context)
    

def blog_detail(request, id=None):
    instance = get_object_or_404(Blog, id=id)
    context = {
        'title': 'List',
        'instance': instance,
    }
    return render(request, 'blog_detail.html', context)


def blog_list(request):
    queryset = Blog.objects.all()
    context = {
        'title': 'List',
        'object_list': queryset,
    }
    return render(request, 'blog_list.html', context)


def blog_update(request, id=None):
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404

    instance = get_object_or_404(Blog, id=id)
    form = BlogForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Successfully Updated')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'title': instance.title,
        'instance': instance,
        'form': form,
    }
    return render(request, 'blog_form.html', context)


def blog_delete(request, id=None):
    if not request.user.is_staff or request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Blog, id=id)
    instance.delete()
    messages.success(request, 'Successfully Deleted')
    return redirect('blog:list')
