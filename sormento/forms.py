from django import forms
from models import *

class MementoForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'name':'editor1', 'id':'editor1'}))

    class Meta:
        model = Memento
        exclude = ('views', 'citation', 'picture',)
#class CategoryForm(forms.ModelForm):
#    name = forms.CharField(max_length=64, help_text="Please enter the source type name.")
#
#    class Meta:
#        model = Category

#class RootForm(forms.ModelForm):
#    class Meta:
#        model = Root
#        exclude = ('user', 'slug',)