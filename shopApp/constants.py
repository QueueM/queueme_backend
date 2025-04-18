# shopApp/constants.py
from django.db import models

class TargetCustomerChoices(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'
    BOTH = 'both', 'Both'

class ServicesTypesChoices(models.TextChoices):
    IN_SHOP = 'in_shop', 'In Shop'
    AT_HOME = 'at_home', 'At Home'
    BOTH = 'both', 'Both'
