from django.shortcuts import render, redirect
from django.http import HttpResponse
import string
from user_profile.models import User
import bcrypt
from random import choice
import base64
import hashlib
import re


def home(request):
    if request.COOKIES.get('auth_cookie'):
        token = base64.standard_b64encode(hashlib.sha256(request.COOKIES.get('auth_cookie').encode()).digest()).decode()
        print(token)
        user = User.objects.filter(token=token).first()
        if user and user.token != '':
            return redirect('/blog/')
    return render(request, 'home/welcome.html')


def register(request):
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    password = request.POST['sign_password']

    checkpass = checkpassvalid(password)
    # print(request.POST['firstname'])
    # return HttpResponse("Please fill out all fields!")

    if User.objects.filter(email=email).exists():
        return HttpResponse("Account already exists with this email")
    elif checkpass[0] and firstname and email:
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        username = (firstname + '_' + lastname + '_' + gentoken())
        username = re.sub('\W+', '_', username)
        # username = username.translate(str.maketrans('', '', string.punctuation))
        user = User(username=username, first_name=firstname, last_name=lastname, email=email, password=password.decode())
        print(user.password)
        user.save()
        return HttpResponse(checkpass[1])
    elif not checkpass[0]:
        return HttpResponse(checkpass[1])
    elif not firstname or not email:
        return HttpResponse("Please fill out all fields!")


# ---- helper funcs ---- #


def checkpassvalid(password):
    haslower = False
    hasupper = False
    hasdigit = False
    haspunc = False
    nowhitespace = True
    properlen = len(password) >= 8
    for char in password:
        if char.islower() and not haslower:
            haslower = True
        if char.isupper() and not hasupper:
            hasupper = True
        if char.isdigit() and not hasdigit:
            hasdigit = True
        if char in string.punctuation and not haspunc:
            haspunc = True
        if char.isspace() and nowhitespace:
            nowhitespace = False
    message = ""
    if not haslower:
        message += "Must have at least 1 lowercase letter<br>"
    if not hasupper:
        message += "Must have at least 1 uppercase letter<br>"
    if not hasdigit:
        message += "Must have at least 1 number<br>"
    if not haspunc:
        message += "Must have at least 1 special letter<br>"
    if not nowhitespace:
        message += "Must not have any whitespace characters (ex. spaces)<br>"
    if not properlen:
        message += "Must be at least 8 characters long <br>"
    if message == "":
        message += "Account successfully registered"
    return [haslower and hasupper and hasdigit and haspunc and nowhitespace and properlen, message]


def gentoken():
    options = string.ascii_letters + string.digits
    token = ''
    for i in range(15):
        token += choice(options)
    return token
