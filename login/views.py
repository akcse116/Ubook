from django.shortcuts import render
import bcrypt
from django.http import HttpResponse
from user_profile.models import User
import string
from random import choice



def home(request):
    data = request.POST.copy()
    pwd = data.get('password').encode()
    email = data.get('email')
    if check_pwd(email,pwd):
        token = gentoken()
        User.objects.get(email = email).token = token
        response = HttpResponse("setting cookie")
        response.set_cookie('auth_cookie', token)
        return response
        
    else:
        print("invalid login")
        return HttpResponse('<h1> invalid login </h1>')


def check_pwd(email, password):
    if User.objects.get(email = email):
        return True
        # figure out !
        # user = User.objects.get(email = email)
        # salt = bcrypt.gensalt()
        # hashed = bcrypt.hashpw(password, salt)
        # if user.password == hashed:
        #     user.token = token
        #     print('logged in')
        #     return True
        # else:
        #     return False

    else:
        return False

def gentoken():
    options = string.ascii_letters + string.digits
    token = ''
    for i in range(15):
        token += choice(options)
    return str(token.encode())
