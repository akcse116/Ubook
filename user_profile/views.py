from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'user_profile/profile_draft.html')
