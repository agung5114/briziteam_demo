# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse,HttpResponseRedirect
from .forms import LoginForm, SignUpForm
# from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# @csrf_exempt
def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login Successful." )
                return redirect("/")
            else:    
                messages.error(request, "Invalid User or Password")  
                return render(request, "login.html", {"form": form})  
        else:
            messages.error(request, "Invalid information.")  
            return render(request, "login.html", {"form": form})  

    return render(request, "login.html", {"form": form})

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = SignUpForm()
    return render (request,"register.html", context={"register_form":form})

# def register_user(request):

#     msg     = None
#     success = False

#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get("username")
#             raw_password = form.cleaned_data.get("password1")
#             user = authenticate(username=username, password=raw_password)

#             msg     = 'User created - please <a href="/login">login</a>.'
#             success = True
            
#             #return redirect("/login/")

#         else:
#             msg = 'Form is not valid'    
#     else:
#         form = SignUpForm()

#     return render(request, "register.html", {"form": form, "msg" : msg, "success" : success })

# @csrf_exempt
def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return HttpResponseRedirect ('/login')
    else:
        return redirect("/")
