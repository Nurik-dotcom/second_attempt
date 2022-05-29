from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('cabinet', lichnyi_cabinet, name="cabinet"),
    path('buy', personal_cabinet, name="buy"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('register', signup_view, name='register'),
    path('', login_request, name='login'),
    path('clear/', clear_history, name='clear')
]
