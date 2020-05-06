from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name = 'login-home'),
    path('logout/', views.logout),
]