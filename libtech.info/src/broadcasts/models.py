from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from django.utils.text import slugify

# Create your models here.

def download_media_location(instance, filename):
        #import pdb; pdb.set_trace()
        # file will be uploaded to MEDIA_ROOT/<id>/<filename> This changed no idea why - Mynk
        # file will be uploaded to MEDIA_ROOT/<slug>/<filename>
        print('%s/%s' % (instance.slug, filename))
        return '%s/%s' % (instance.slug, filename)
    
class Broadcast(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='broadcast_managers', blank=True)
    media = models.FileField(
        blank=True,
        null=True,
        upload_to=download_media_location,
        storage=FileSystemStorage(location=settings.PROTECTED_ROOT)
    )
    name = models.CharField(max_length=30)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField(default='Enter description here')
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # print('%s' % self.slug)
        return reverse('broadcasts:detail_slug', kwargs = {'slug': self.slug})
        # return '/broadcasts/%s/' % (self.slug)

    def get_download(self):
        return reverse('broadcasts:download_slug', kwargs = {'slug': self.slug})

def create_slug(instance, new_slug=None):
    if new_slug:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    qs = Broadcast.objects.filter(slug=slug) 
    if qs.exists():
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug)

    return slug
    
def broadcast_pre_save_receiver(sender, instance, *args, **kwargs):
    #print('sender[%s], instance[%s]' % (sender, instance))
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(broadcast_pre_save_receiver, sender=Broadcast)

'''
def broadcast_post_save_receiver(sender, instance, *args, **kwargs):
    #print('sender[%s], instance[%s]' % (sender, instance))
    slug = slugify(instance.name)
    if instance.slug != slug:
        instance.slug = slug
        instance.save()

post_save.connect(broadcast_post_save_receiver, sender=Broadcast)
'''

class MyBroadcasts(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    broadcasts = models.ManyToManyField(Broadcast, blank=True)

    def __str__(self):
        return str(self.broadcasts.count())
    
    class Meta:
        verbose_name = 'My Broadcasts'
        verbose_name_plural = 'My Broadcasts'
