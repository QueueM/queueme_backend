# File: companyApp/urls.py

from django.urls import path
from .views import RegisterAsCompanyAPIView

urlpatterns = [
    path('register/', RegisterAsCompanyAPIView.as_view(), name='company-register'),
    # add other companyApp endpoints here
]
