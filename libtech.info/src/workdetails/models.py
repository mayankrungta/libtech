from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from django.utils.text import slugify

# Create your models here.
    
class Workdetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='workdetail_managers', blank=True)
    slug = models.SlugField(blank=True, unique=True)

    block_name = models.CharField(max_length=30)
    block_code = models.CharField(max_length=3)
    panchayat_name = models.CharField(max_length=40)
    panchayat_code = models.CharField(max_length=3)
    financial_year = models.CharField(max_length=2)
    muster_index = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=256)
    jobcard = models.CharField(max_length=30)
    jobcard_number = models.PositiveSmallIntegerField()
    muster_number = models.CharField(max_length=50)
    work_code = models.CharField(max_length=40)
    work_name = models.CharField(max_length=1024)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    days_worked = models.PositiveSmallIntegerField()
    day_wage = models.IntegerField()
    total_wage = models.IntegerField()
    account_number = models.CharField(max_length=25)
    wagelist_number = models.CharField(max_length=20)
    bank_or_po_name = models.CharField(max_length=40)
    branch_name_or_po_address = models.CharField(max_length=40)
    branch_or_po_code = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    credited_date = models.DateTimeField(null=True)
    is_bank = models.BooleanField()
    is_post = models.BooleanField()
    
    rejection_reason = models.CharField(max_length=50, null=True)
    fto_event_date = models.DateTimeField(null=True)
    fto_event = models.CharField(max_length=2048, null=True)
    fto_office = models.CharField(max_length=1024, null=True)
    fto_field = models.CharField(max_length=2048, null=True)

    update_date = models.DateTimeField()
    create_date = models.DateTimeField()

    fto_number = models.CharField(max_length=30, null=True)
    fto_number_updated = models.BooleanField()
    primary_account_holder = models.CharField(max_length=50, null=True)
    payment_date = models.DateTimeField(null=True)

    #FIXME TBD Mynk
    is_closed = models.BooleanField(default='False')
    remarks = models.CharField(max_length=30, default='Add your remarks here')

    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # print('%s' % self.slug)
        return reverse('workdetails:detail_slug', kwargs = {'slug': self.slug})
        # return '/workdetails/%s/' % (self.slug)

    def get_download(self):
        return reverse('workdetails:download_slug', kwargs = {'slug': self.slug})

def create_slug(instance, new_slug=None):
    if new_slug:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    qs = Workdetail.objects.filter(slug=slug) 
    if qs.exists():
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug)

    return slug
    
def workdetail_pre_save_receiver(sender, instance, *args, **kwargs):
    #print('sender[%s], instance[%s]' % (sender, instance))
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(workdetail_pre_save_receiver, sender=Workdetail)

class MyWorkdetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    workdetails = models.ManyToManyField(Workdetail, blank=True)

    def __str__(self):
        return str(self.workdetails.count())
    
    class Meta:
        verbose_name = 'My Workdetails'
        verbose_name_plural = 'My Workdetails'
