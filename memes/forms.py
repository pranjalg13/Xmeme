from django.forms import ModelForm
from django import forms
from .models import CreateMeme


# Form for NewMeme
class MemeForm(forms.ModelForm):

    class Meta:
        model = CreateMeme
        fields = ['name','caption','url']
    def __init__(self, *args, **kwargs):
        super(MemeForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter the Owner Name'
        self.fields['caption'].widget.attrs['placeholder'] = 'Enter the caption for the meme'
        self.fields['url'].widget.attrs['placeholder'] = 'Enter the URL of the image'
        


# UpdateForm of Meme
class UpdateMemeForm(forms.ModelForm):
    class Meta:
        model = CreateMeme
        fields = ['name','caption','url']

    def save(self, commit = True):
        meme =  self.instance
        meme.caption = self.cleaned_data['caption']
        meme.url = self.cleaned_data['url']
        if commit:
            meme.save()
        return meme