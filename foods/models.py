from django.db import models
from users.models import User


class LabelNutrients(models.Model):
    fat = models.FloatField(default=0.0)
    saturated_fat = models.FloatField(default=0.0)
    trans_fat = models.FloatField(default=0.0)
    cholesterol = models.FloatField(default=0.0)
    sodium = models.FloatField(default=0.0)
    carbohydrates = models.FloatField(default=0.0)
    fiber = models.FloatField(default=0.0)
    sugars = models.FloatField(default=0.0)
    protein = models.FloatField(default=0.0)
    calcium = models.FloatField(default=0.0)
    iron = models.FloatField(default=0.0)
    potassium = models.FloatField(default=0.0)
    calories = models.FloatField(default=0.0)


class Nutrient(models.Model):
    id = models.IntegerField(primary_key=True)
    number = models.FloatField()
    name = models.CharField()
    rank = models.IntegerField()
    unit_name = models.CharField()


class FoodNutrient(models.Model):
    id = models.IntegerField(primary_key=True)
    amount = models.FloatField()
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)


class AbridgedBrandedFoodItem(models.Model):
    fdc_id = models.IntegerField(primary_key=True)
    brand_owner = models.CharField()
    description = models.CharField()
    ingredients = models.CharField(default="")
    serving_size = models.FloatField()
    serving_size_unit = models.CharField()
    label_nutrients = models.OneToOneField(LabelNutrients, on_delete=models.CASCADE, null=True)
    food_nutrients = models.ManyToManyField(FoodNutrient)


class UserFoodRestriction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(AbridgedBrandedFoodItem, on_delete=models.CASCADE)
    reason = models.CharField(null=True)

    class Meta:
        unique_together = ("user", "food")


class UserFoodPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(AbridgedBrandedFoodItem, on_delete=models.CASCADE)
    dislikes = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "food")
