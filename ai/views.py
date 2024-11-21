from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from openai import OpenAI
from .serializers import ChatBotQuerySerializer, ChatBotResponseSerializer
from drf_spectacular.utils import extend_schema
from foods.models import UserFoodPreference, UserFoodRestriction
from users.models import UserFitnessProfile
from users.serializers import UserFitnessProfileSerializer
from django.core.exceptions import ObjectDoesNotExist
from foods.serializers import ResponseDetailSerializer
import json


class GetChatBotResponseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=ChatBotQuerySerializer,
        responses={200: ChatBotResponseSerializer, 400: ResponseDetailSerializer},
    )
    def post(self, request):
        serializer = ChatBotQuerySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                ResponseDetailSerializer({"detail": "Invalid input"}),
                status=status.HTTP_400_BAD_REQUEST,
            )

        food_preferences = UserFoodPreference.objects.filter(user=request.user).values_list(
            "food__description", "dislikes"
        )
        food_pref_json = json.dumps([{"d": p[0], "dl": p[1]} for p in food_preferences])

        food_restrictions = UserFoodRestriction.objects.filter(user=request.user).values_list(
            "food__description", "reason"
        )
        food_res_json = json.dumps([{"d": r[0], "r": r[1]} for r in food_restrictions])

        try:
            fitness_profile = UserFitnessProfile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            fitness_profile = None

        if fitness_profile != None:
            fitness_prof_json = UserFitnessProfileSerializer(fitness_profile).data
        else:
            fitness_prof_json = ""

        sys_prompt = (
            "You are a nutrition assistant, you help users meet their fitness goals. "
            f"My goals are given here {fitness_prof_json}. All values are measured in metric units. "
            "If my prompt is about recipes or meal planning, refer to my preferences and restrictions "
            "when answering. Preferences, where d is the description of the food and dl is true if I "
            f"dislike the food and false if I like it: {food_pref_json} disliked foods should be avoided and liked "
            "foods should only be added where appropriate for the recipe."
            "Restrictions, where d is the description of the food and "
            f"r is the reason for the restriction: {food_res_json}"
            "If one of my restricted foods is part of a recipe, substitute it for something similar and remove the restricted item from the ingredients list. "
            "the ingredient was substituted. "
            "Example: almonds instead of peanuts if peanuts are restricted. "
            "Include a calorie and macronutrient estimation at the end of the recipe. "
            "Your response must be in the following JSON format: "
            '{"type": "recipe", "recipe": "Detailed instructions go here", "ingredients": [{"description": eggs, "amount:" 2, "unit": "whole"}], '
            '"est_carbs": 90, "est_fat": 20, "est_protein": 25, "est_calories": 650}'
            "Do not include any text before the valid JSON. The message should start with the opening bracket of the JSON response. "
            "Remember to make the recipe valid markdown. "
            "In the example above, all values with keys starting with 'est' are your estimates for the associated values. "
            'ingredients is a list of JSON objects of the form {"description": "description of food", "amount": 5, "unit": "grams"}'
            "Amount should be the amount of the ingredient used and unit should match the unit "
            "given in the recipe (i.e. grams, ounces, etc.)"
            "The Recipe must be markdown."
            "If the prompt is not about a recipe, the response should be in the following JSON format: "
            '{"type": "message", message: "message containing markdown"} '
            'Recipes must always have "recipe" as the type value and non-recipes must always have "message" as the type value.'
        )

        user_prompt = serializer.validated_data["query"]

        client = OpenAI()

        bot_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        print(bot_response.choices[0].message.content)

        return Response(
            ChatBotResponseSerializer(json.loads(bot_response.choices[0].message.content)).data,
            status.HTTP_200_OK,
        )
