from django import forms

from .models import Comment,Post


class TicketForm(forms.Form):
    author_name = forms.CharField(max_length=30)
    author_email = forms.EmailField()
    title = forms.CharField(max_length=30)
    body = forms.CharField(max_length=300,widget=forms.TextInput)

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=["body"]
        widgets={
            'body':forms.Textarea
        }
class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=["title","description"]
        widgets={
            "description":forms.Textarea
        }
class Search(forms.Form):
    query=forms.CharField(max_length=50)
