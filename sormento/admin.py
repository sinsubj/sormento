from django.contrib import admin
from models import *
from django_mptt_admin.admin import DjangoMpttAdmin
from django import forms
from models import *


class MementoAdmin(admin.ModelAdmin):
    formfield_overrides = { models.TextField:
                               {'widget':
                                    forms.Textarea(attrs={'class':'ckeditor'})
                               },
                           }
    list_display = ['source', 'text']

    class Media:
        js = ('/static/ckeditor/ckeditor.js',)

admin.site.register(Source, DjangoMpttAdmin)
admin.site.register(Memento, MementoAdmin)

#class SourceInline(admin.StackedInline):
#    model = Source
#
#class SourceAdmin(admin.ModelAdmin):
#    inlines = [
#        SourceInline,
#    ]