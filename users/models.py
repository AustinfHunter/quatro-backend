import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class UserFitnessProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    current_weight = models.FloatField(null=True, blank=True)
    goal_weight = models.FloatField(null=True, blank=True)
    activity_level_choices = {
        0: "Sedentary",
        1: "Inactive",
        2: "Somewhat Active",
        3: "Active",
        4: "Very Active",
    }
    activity_level = models.IntegerField(choices=activity_level_choices, null=True, blank=True)
    daily_calorie_goal = models.IntegerField(null=True, blank=True)
