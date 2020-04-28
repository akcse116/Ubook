from django.shortcuts import render

from django.http import HttpResponse
from user_profile.models import User
import string
from django.contrib.auth.hashers import BCryptSHA256PasswordHasher


def home(request):
    return render(request, 'login/login.html')


def register(request):
    username = request.POST['username']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    password = request.POST['sign_password']

    checkpass = checkpassvalid(password)

    if checkpass[0] and username and firstname and lastname and email:
        user = User(username=username, firstname=firstname, lastname=lastname, email=email, password=password)
        print(user.password)
        user.save()
        return HttpResponse(checkpass[1])
    elif not checkpass[0]:
        return HttpResponse(checkpass[1])
    elif not username or not firstname or not lastname or not email:
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
