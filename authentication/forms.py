# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, ValidationError
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))
    def check_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username__iexact=data).exists():
            raise ValidationError('Username exists')
        return data

    def compare_passwords(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['password_confirm']
        if password2 != password1:
            raise ValidationError('Password does not match')
        return password1
	
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.TextInput()
    last_name = forms.TextInput()
    class Meta:
        model = User
        fields = ("username","first_name","last_name","email", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    def check_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username__iexact=data).exists():
            raise ValidationError('Username exists')
        return data

    def compare_passwords(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['password_confirm']
        if password2 != password1:
            raise ValidationError('Password does not match')
        return password1
