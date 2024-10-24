from django.db import models
from users.models import User


class UserFoodRestriction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fdc_id = models.IntegerField(null=True)
    reason = models.CharField(null=True)

    class Meta:
        unique_together = ("user", "fdc_id")


class UserFoodPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fdc_id = models.IntegerField(null=True)
    dislikes = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "fdc_id")


class LabelNutrients(models.Model):
    fat = models.FloatField()
    saturated_fat = models.FloatField()
    trans_fat = models.FloatField()
    cholesterol = models.FloatField()
    sodium = models.FloatField()
    carbohydrates = models.FloatField()
    fiber = models.FloatField()
    sugars = models.FloatField()
    protein = models.FloatField()
    calcium = models.FloatField()
    iron = models.FloatField()
    potassium = models.FloatField()
    calories = models.FloatField()


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
