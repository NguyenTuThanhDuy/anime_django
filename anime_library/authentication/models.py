from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserAccountInfo(models.Model):
    user_account = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    date_of_birth = models.CharField(max_length=16)
    phone_number = models.CharField(max_length=20, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
