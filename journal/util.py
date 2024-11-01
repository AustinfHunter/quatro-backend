from foods.models import FoodNutrient


def getNutrientAmountOrZero(nutrients: FoodNutrient, nutrient_name):
    try:
        return nutrients.get(nutrient__name=nutrient_name).amount
    except nutrients.model.DoesNotExist:
        return 0.0
