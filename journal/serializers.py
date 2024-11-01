from rest_framework import serializers
from .models import UserFoodJournalEntry
from foods.serializers import AbridgedBrandedFoodSerializer
from users.models import UserFitnessProfile


class UserFoodJournalEntrySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    food = AbridgedBrandedFoodSerializer()

    class Meta:
        model = UserFoodJournalEntry
        fields = ["id", "user", "date", "amount_consumed_grams", "food"]


class UserFoodJournalEntryDTOSerializer(serializers.Serializer):
    fdc_id = serializers.IntegerField()
    amount_consumed_grams = serializers.FloatField()
    date = serializers.DateField(required=False)


class UserFoodJournalEntryListSerializer(serializers.Serializer):
    journal_entries = UserFoodJournalEntrySerializer(many=True)


class UserDailyMacrosSerializer(serializers.Serializer):
    total_calories = serializers.FloatField()
    total_carbs = serializers.FloatField()
    total_fat = serializers.FloatField()
    total_protein = serializers.FloatField()
    daily_calorie_limit = serializers.FloatField()


class UserDashboardSerializer(serializers.Serializer):
    journal_entries = UserFoodJournalEntrySerializer(many=True)
    daily_macros = serializers.SerializerMethodField()

    def get_daily_macros(self, obj) -> UserDailyMacrosSerializer:
        user = self.context.get("user")
        date = self.context.get("date")
        entries = UserFoodJournalEntry.objects.filter(user=user, date=date)
        total_calories = 0.0
        total_carbs = 0.0
        total_fat = 0.0
        total_protein = 0.0
        for entry in entries:
            nutrients = entry.food.food_nutrients
            cal_amount = nutrients.get(nutrient__name="Energy").amount
            carbs_amount = nutrients.get(nutrient__name="Carbohydrate, by difference").amount
            fat_amount = nutrients.get(nutrient__name="Total lipid (fat)").amount
            protein_amount = nutrients.get(nutrient__name="Protein").amount
            total_calories += (cal_amount / 100) * entry.amount_consumed_grams
            total_carbs += (carbs_amount / 100) * entry.amount_consumed_grams
            total_fat += (fat_amount / 100) * entry.amount_consumed_grams
            total_protein += (protein_amount / 100) * entry.amount_consumed_grams

        try:
            daily_cals = UserFitnessProfile.objects.get(
                user=self.context.get("user")
            ).get_daily_cals()
        except UserFitnessProfile.DoesNotExist():
            daily_cals = None

        return UserDailyMacrosSerializer(
            {
                "total_calories": total_calories,
                "total_carbs": total_carbs,
                "total_fat": total_fat,
                "total_protein": total_protein,
                "daily_calorie_limit": daily_cals,
            }
        ).data
