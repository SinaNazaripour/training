from django import forms

class TicketForm(forms.Form):
    author_name = forms.CharField(max_length=30)
    author_email = forms.EmailField()
    title = forms.CharField(max_length=30)
    body = forms.CharField(max_length=300,widget=forms.TextInput)

