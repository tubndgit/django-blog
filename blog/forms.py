from .models import Comment, Contact
from django import forms
from django.utils.translation import ugettext_lazy as _

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('contact_name', 'contact_email', 'content')
        labels = {
            'contact_name': _('Your Name'),
            'contact_email': _('Email Address'),
            'content': _('Message'),
        }
