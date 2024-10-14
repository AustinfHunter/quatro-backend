from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .serializers import CredentialsSerializer, UserSerializer, SignupSerializer
from .validators import validate_registration_passwords
from drf_yasg.utils import swagger_auto_schema


class SignUpView(APIView):
    """API Endpoint for handling new user signups"""

    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(request_body=SignupSerializer, responses={201: UserSerializer})
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

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        pass
