import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.BinaryField(max_length=60)


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
