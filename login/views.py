from django.shortcuts import render

from django.http import HttpResponse
from user_profile.models import User
import string
from django.contrib.auth.hashers import BCryptSHA256PasswordHasher


def home(request):
    return render(request, 'login/login.html')

