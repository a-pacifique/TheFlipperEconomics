from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Article, User
from tinymce.widgets import TinyMCE


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}, mce_attrs={'entity_encoding': 'raw'}))

    class Meta:
        model = Article
        fields = ['title', 'image', 'content', 'published']
        labels = {
            'image': 'Article Image',
            'content': 'Article Content',
            'published': 'Publish Article',
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Your Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=200, label='Subject', widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Your Message', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))



