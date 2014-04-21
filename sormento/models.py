from django.db import models
from django.contrib.auth.models import User
from unidecode import unidecode
from django.template.defaultfilters import slugify
from mptt.models import MPTTModel, TreeForeignKey


class Source(MPTTModel):
    PICTURE_DIR = 'source_images'

    user = models.ForeignKey(User)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    root = models.CharField(max_length=64, blank=True)
    title = models.CharField(max_length=128)
    by = models.CharField(max_length=128, blank=True)
    picture = models.ImageField(upload_to=PICTURE_DIR, blank=True)
    date_added = models.DateField(auto_now_add=True)
    date_produced = models.DateField(blank=True, null=True)
    url = models.URLField(blank=True)
    remark = models.TextField(blank=True)
    slug = models.SlugField(blank=True)

    def __unicode__(self):
        if self.is_root_node():
            return self.title
        else:
            return "%s > %s" % (self.parent, self.title)

    def save(self, *args, **kwargs):
        #if not self.id:
        #    # slugify only if newly created object because otherwise urls would change
        self.slug = slugify(unidecode(self.title))
        self.root = self.__unicode__()
        # if self.parent:
        #     self.root = self.parent.get_root().title
        # else:
        #     self.root = self.title
        super(Source, self).save(*args, **kwargs)

#class Source(models.Model):
#    root = models.ForeignKey(Root)
#    title = models.CharField(max_length=128, blank=True)        # volume, article title, season and episode, etc.
#    author = models.CharField(max_length=64, blank=True)
#    published_date = models.DateField(blank=True, null=True)                  # should change it to MM/DD/YY or something like that later
#    url = models.URLField(blank=True)
#
#    def __unicode__(self):
#        return "%s: %s" % (self.root, self.title)

#class MementoType(models.Model):
#    name = models.CharField(max_length=64)                      # quote, passage, excerpt, etc.
#
#    def __unicode__(self):
#        return self.name

class Memento(models.Model):
    PICTURE_DIR = 'memento_images'
    QUOTE = 'QT'
    EXCERPT = 'EX'
    NOTES = 'NS'
    MEMENTO_TYPE_CHOICES = (
        (QUOTE, 'Quote'),
        (EXCERPT, 'Excerpt'),
        (NOTES, 'Notes'),
    )

    source = models.ForeignKey(Source, help_text="Source")
    type = models.CharField(max_length=2, choices=MEMENTO_TYPE_CHOICES, default=NOTES, help_text="Type")
    title = models.CharField(max_length=128, blank=True, help_text="Title")
    by = models.CharField(max_length=128, blank=True, help_text="By")
    text = models.TextField(blank=True, help_text="Content")
    picture = models.ImageField(upload_to=PICTURE_DIR, blank=True, help_text="Picture")
    url = models.URLField(blank=True, help_text="URL")
    citation = models.CharField(max_length=128, blank=True)
    date_added = models.DateField(auto_now_add=True)
    date_produced = models.DateField(blank=True, null=True, help_text="Date Produced")
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s, %s" % (self.text, self.source)


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username