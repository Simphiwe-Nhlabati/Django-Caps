from .models import Publisher, Article
from django import forms


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['user',
                  'name', 
                  'editors', 
                  'journalists']
        # widgets = {
        #     'editors': forms.CheckboxSelectMultiple(),
        #     'journalists': forms.CheckboxSelectMultiple(),
        # }
        # labels = {
        #     'name': 'Publisher Name',
        #     'editors': 'Editors',
        #     'journalists': 'Journalists',
        # }
        

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title',
                  'description',
                  'image',
                  'content']
        
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['placeholder'] = 'Enter article title'
        self.fields['title'].label = 'Article Title'
        self.fields['title'].help_text = '<span class="form-text text-muted"><small>Required. 200 characters or fewer.</small></span>'
        
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter article description'
        self.fields['description'].label = 'Description'
        self.fields['description'].help_text = '<span class="form-text text-muted"><small>Required. 500 characters or fewer.</small></span>'
        
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['placeholder'] = 'Upload article image'
        self.fields['image'].label = 'Image'
        self.fields['image'].help_text = '<span class="form-text text-muted"><small>Optional. Upload an image for the article.</small></span>'
        
        self.fields['content'].widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs['placeholder'] = 'Enter article content'
        self.fields['content'].label = 'Content'
        self.fields['content'].help_text = '<span class="form-text text-muted"><small>Required. The content of the article.</small></span>'
        
        # widgets = {
        #     'journalist': forms.CheckboxSelectMultiple(),
        # }
        # labels = {
        #     'title': 'Article Title',
        #     'content': 'Content',
        #     'publisher': 'Publisher',
        #     'journalist': 'Journalists',
        # }
        

