from django.urls import path
from .views import create_user,fetch_users

urlpatterns = [
    path('create_user/', create_user),
    path('fetch_users/', fetch_users)

]
