from . import views
from django.urls import path
from .views import send_friend_request, accept_request


urlpatterns = [
    path('', views.home, name='profile-home'),
    path('add-friend/<int:id>/', send_friend_request, name='add-friend'),
    path('accept/<int:id>/', accept_request, name='accept'),
]