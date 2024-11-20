from django.urls import path
from .views import UserView

urlpatterns = [
    path('users', UserView.as_view()),  # For POST and fetching all users
    path('users/<str:user_id>', UserView.as_view(),name='user_detail'),
]
