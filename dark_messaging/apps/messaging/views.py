from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.contrib import messages
import bcrypt
import datetime
import time
from django.contrib.sessions.models import Session
today = datetime.date.today()



def index(request):
    return render(request, 'messaging/index.html')

def process(request):
    print request.POST
    errors = User.objects.validator(request.POST)
    if errors:
        for error in errors:
            print errors[error]
            messages.error(request, errors[error])
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name = request.POST['name'], email = request.POST['email'], password = hashed_pw, dob = request.POST['date'])
        request.session['id'] = user.id
    return redirect('/home')

def login(request):
    login_return = User.objects.login(request.POST)
    if 'user' in login_return:
        request.session['id'] = login_return['user'].id
        messages.success(request, "You have successfully logged in")
        return redirect('/home')
    else:
        messages.error(request, login_return['error'])
    return redirect('/')

def logout(request):
    Session.objects.all().delete()
    return redirect('/')

def home(request):
    return render(request, 'messaging/home.html')