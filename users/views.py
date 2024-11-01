from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .serializers import (
    UserSerializer,
    SignupSerializer,
    AccountSerializer,
    UserFitnessProfileSerializer,
)
from .validators import validate_registration_passwords
from foods.serializers import ResponseDetailSerializer
from drf_spectacular.utils import extend_schema

from .models import User, UserFitnessProfile


class SignUpView(APIView):
    """API Endpoint for handling new user signups"""

    permission_classes = [permissions.AllowAny]

    @extend_schema(request=SignupSerializer, responses={201: UserSerializer})
    def post(self, request):
        try:
            validate_registration_passwords(request.data)
        except ValidationError as e:
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)
        userModel = get_user_model()
        signupData = SignupSerializer(data=request.data)

        if signupData.is_valid():
            validated_data = signupData.validated_data
            print(validated_data)
            if userModel.objects.filter(email=validated_data["email"]).exists():
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            user = signupData.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class AccountView(APIView):
    """API Endpoint for user account information"""

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: AccountSerializer, 404: ResponseDetailSerializer})
    def get(self, request):
        print(request.user.id)
        user = get_object_or_404(User, id=request.user.id)
        try:
            fitness_profile = UserFitnessProfile.objects.get(user__id=request.user.id)
        except UserFitnessProfile.DoesNotExist:
            fitness_profile = None
        return Response(
            AccountSerializer({"user_details": user, "fitness_profile": fitness_profile}).data,
            status=status.HTTP_200_OK,
        )


class FitnessProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=UserFitnessProfileSerializer,
        responses={200: UserFitnessProfileSerializer, 404: ResponseDetailSerializer},
    )
    def put(self, request, fitness_profile_id):
        serializer = UserFitnessProfileSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            fitness_profile = serializer.save()
            return Response(
                UserFitnessProfileSerializer(fitness_profile).data, status.HTTP_202_ACCEPTED
            )
        return Response(
            ResponseDetailSerializer({"detail": "Could not update fitness profile."}),
            status=status.HTTP_400_BAD_REQUEST,
        )


class CreateFitnessProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=UserFitnessProfileSerializer,
        responses={201: UserFitnessProfileSerializer, 404: ResponseDetailSerializer},
    )
    def post(self, request):
        serializer = UserFitnessProfileSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            fitness_profile = serializer.save()
            return Response(
                UserFitnessProfileSerializer(fitness_profile).data, status=status.HTTP_201_CREATED
            )
        print(serializer.errors)
        return Response(
            ResponseDetailSerializer({"detail": "Could not create fitness profile."}).data,
            status=status.HTTP_400_BAD_REQUEST,
        )
