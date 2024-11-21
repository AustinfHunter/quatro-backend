from rest_framework import serializers


class ChatBotQuerySerializer(serializers.Serializer):
    query = serializers.CharField()


class IngredientSerializer(serializers.Serializer):
    description = serializers.CharField()
    amount = serializers.IntegerField()
    unit = serializers.CharField()


class ChatBotResponseSerializer(serializers.Serializer):
    type = serializers.CharField()
    message = serializers.CharField(required=False)
    recipe = serializers.CharField(required=False)
    ingredients = IngredientSerializer(many=True, required=False)
    est_carbs = serializers.IntegerField(required=False)
    est_protein = serializers.IntegerField(required=False)
    est_fat = serializers.IntegerField(required=False)
    est_calories = serializers.IntegerField(required=False)
