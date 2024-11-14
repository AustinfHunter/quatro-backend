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


class ActivityLevelChoices(models.IntegerChoices):
    N_ACTIVE = 0, "Sedentary"
    L_ACTIVE = 300, "Lightly Active"
    M_ACTIVE = 500, "Moderately Active"
    V_ACTIVE = 700, "Very Active"


class SexChoices(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"


class UserFitnessProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    sex = models.CharField(choices=SexChoices, null=True)
    age = models.IntegerField(null=True)
    current_weight = models.FloatField(null=True, blank=True)
    height = models.IntegerField(null=True)
    goal_weight_velocity = models.FloatField(null=True)
    goal_weight = models.FloatField(null=True, blank=True)
    activity_level = models.IntegerField(choices=ActivityLevelChoices, null=True, blank=True)
    daily_calorie_goal = models.FloatField(null=True)

    def get_daily_cals(self):
        if self.sex == "male":
            adj = 5
        else:
            adj = -161

        bmr = 10 * self.current_weight + 6.25 * self.height + 5 * self.age + adj
        delta_cals = (self.goal_weight_velocity * 7716.179) / 7

        return bmr + delta_cals + self.activity_level

