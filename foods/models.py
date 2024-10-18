from django.db import models
from users.models import User


class UserFoodRestriction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fdc_id = models.IntegerField(null=True)
    reason = models.CharField(null=True)


class UserFoodPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fdc_id = models.IntegerField(null=True)
    dislikes = models.BooleanField(default=False)
