# File: usersapp/urls.py

from django.urls import path
from .views import (
    UpdateProfileSuggestAPIView,
    RegisterUserAPIView,
    UserMasterDetailsAPIView,
)

urlpatterns = [
    path('update-profile-suggest/', UpdateProfileSuggestAPIView.as_view(), name='update-profile-suggest'),
    path('register/', RegisterUserAPIView.as_view(), name='register-user'),
    path('master-details/', UserMasterDetailsAPIView.as_view(), name='user-master-details'),
]