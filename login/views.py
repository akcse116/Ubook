from django.shortcuts import render,redirect
import bcrypt
from django.http import HttpResponse
from user_profile.models import User
import string
from random import choice
import base64
import hashlib


def home(request):
    if request.POST:
        data = request.POST.copy()
        pwd = data.get('password').encode()
        email = data.get('email')
        print(data)
        if check_pwd(email,pwd):
            token = gentoken()
            response = HttpResponse("setting cookie")
            response.set_cookie('auth_cookie', token)
            token = base64.standard_b64encode(hashlib.sha256(token.encode()).digest()).decode()
            user = User.objects.get(email=email)
            user.token = token
            user.save()
            return response
        else:
            print("invalid login")
            return HttpResponse('invalid login')
    else:
        print("invalid login")
        response = redirect('/')
        return response
        # return HttpResponse('invalid login')


def check_pwd(email, password):
    if User.objects.get(email=email):
        # return True
        # figure out !
        user = User.objects.get(email=email)
        if bcrypt.checkpw(password, user.password.encode()):
            print('logged in')
            return True
        else:
            return False
    else:
        return False


def gentoken():
    options = string.ascii_letters + string.digits
    token = ''
    for i in range(15):
        token += choice(options)
    return str(token.encode())


def logout(request):
    if request.COOKIES.get('auth_cookie'):
        token = base64.standard_b64encode(hashlib.sha256(request.COOKIES.get('auth_cookie').encode()).digest()).decode()
        print(token)
        user = User.objects.filter(token=token).first()
        if user and user.token != '':
            user.token = ''
            user.save()
        response = redirect('/')
        response.delete_cookie('auth_cookie')
    return redirect('/')