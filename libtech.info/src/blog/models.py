from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=120);
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'id': self.id})
