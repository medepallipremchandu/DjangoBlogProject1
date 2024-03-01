# blog/forms.py

from django import forms

class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Name"}
        ),
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Leave a comment!"}
        )
    )

class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(label='Your Message', widget=forms.Textarea)



from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
 
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_no = forms.CharField(max_length = 20)
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'first_name', 'last_name' ,'password1', 'password2']