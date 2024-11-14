from rest_framework import serializers


class ChatBotQuerySerializer(serializers.Serializer):
    query = serializers.CharField()


class IngredientSerializer(serializers.Serializer):
    description = serializers.CharField()
    amount = serializers.IntegerField()
    unit = serializers.CharField()

class ChatBotResponseSerializer(serializers.Serializer):
    recipe = serializers.CharField()
    ingredients = IngredientSerializer(many=True)
    est_carbs = serializers.IntegerField()
    est_protein = serializers.IntegerField()
    est_fat = serializers.IntegerField()
    est_calories = serializers.IntegerField()
