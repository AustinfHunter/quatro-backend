from django.db import models
from users.models import User
from foods.models import AbridgedBrandedFoodItem


class UserFoodJournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(AbridgedBrandedFoodItem, on_delete=models.CASCADE)
    date = models.DateField()
    amount_consumed_grams = models.FloatField()
