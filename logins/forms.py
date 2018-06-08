from django import forms
from django.contrib.auth.models import User
import re

class RegForm(forms.Form):
    first_name = forms.CharField(label = "First Name", max_length=120)
    last_name = forms.CharField(label = "Last Name", max_length=120)
    email = forms.CharField(label="Email", widget=forms.EmailInput)
    phone = forms.CharField(label="Phone No")
    username = forms.CharField(label="UserName", max_length=120)
    pword = forms.CharField(label="Password", max_length=32, widget = forms.PasswordInput)
    pword_r = forms.CharField(label="Confirm Password", max_length=32, widget=forms.PasswordInput)

    def clean(self):
        pw = self.cleaned_data['pword']
        pwr = self.cleaned_data['pword_r']

        if pw != pwr:
            raise forms.ValidationError({'pword': ['Password mismatch',]})
        if len(pw) < 6:
            raise forms.ValidationError({'pword': ['Password must be 6 characters long']})

        return self.cleaned_data

    def clean_username(self):
        uname = self.cleaned_data['username']
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError('Username already exist')
        return uname

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) < 6 or len(phone) > 12:
            raise forms.ValidationError('Invalid Phone number')
        for c in phone:
            if not c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+']:
                raise forms.ValidationError('Phone number should contain 0-9 and + symbols')
        return phone

    def clean_first_name(self):
        fn = self.cleaned_data['first_name']
        if len(fn) <= 0:
            raise forms.ValidationError('This field is required')
        return fn

    def clean_last_name(self):
        fn = self.cleaned_data['last_name']
        if len(fn) <= 0:
            raise forms.ValidationError('This field is required')
        return fn

    def clean_email(self):
        em = self.cleaned_data['email']
        email_re = re.compile(
                            r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
                            r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
                            r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)  # domain
        if not email_re.match(em):
            raise forms.ValidationError('Please enter a valid email')
        return em

class LoginForm(forms.Form):
    username = forms.CharField(label="UserName", max_length=120)
    password = forms.CharField(label="Password", max_length=32, widget=forms.PasswordInput)
    pass