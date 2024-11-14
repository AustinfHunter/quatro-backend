from .models import User, UserFitnessProfile
from rest_framework import serializers


class CredentialsSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        return User(**validated_data)


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def create(self, validated_data):
        user = User(
            is_superuser=False,
            email=validated_data.get("email").lower(),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
        )

        user.set_password(validated_data.get("password"))
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]


class UserFitnessProfileSerializer(serializers.ModelSerializer):
    daily_calorie_goal = serializers.SerializerMethodField()

    class Meta:
        model = UserFitnessProfile
        fields = [
            "age",
            "sex",
            "current_weight",
            "height",
            "goal_weight",
            "goal_weight_velocity",
            "activity_level",
            "daily_calorie_goal",
        ]

    def create(self, validated_data):
        p = UserFitnessProfile()
        p.user = self.context.get("user")
        p.current_weight = validated_data["current_weight"]
        p.goal_weight = validated_data["goal_weight"]
        p.height = validated_data["height"]
        p.goal_weight_velocity = validated_data["goal_weight_velocity"]
        p.sex = validated_data["sex"]
        p.age = validated_data["age"]
        p.activity_level = validated_data["activity_level"]
        p.save()
        return p

    def get_daily_calorie_goal(self, obj: UserFitnessProfile) -> float:
        if obj.sex == "male":
            adj = 5
        else:
            adj = -161

        bmr = 10 * obj.current_weight + 6.25 * obj.height + 5 * obj.age + adj
        delta_cals = (obj.goal_weight_velocity * 7716.179) / 7

        return bmr + delta_cals + obj.activity_level


class AccountSerializer(serializers.Serializer):
    user_details = UserSerializer()
    fitness_profile = UserFitnessProfileSerializer(required=False)
