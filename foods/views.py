from rest_framework.views import APIView, Response
from rest_framework import permissions, status
from drf_spectacular.utils import extend_schema, PolymorphicProxySerializer, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from .fdcclient import get_fdc_client
from .models import UserFoodPreference, UserFoodRestriction
from .serializers import (
    BrandedFoodItemSerializer,
    FoundationFoodItemSerializer,
    AbridgedFoodItemSerializer,
    UserFoodPreferenceSerializer,
    UserFoodRestrictionSerializer,
    UserFoodPreferencesDTOSerializer,
    UserFoodRestrictionDTOSerializer,
    ErrorSerializer,
)

fdc_client = get_fdc_client()


class GetFoodsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={
            200: PolymorphicProxySerializer(
                component_name="Food",
                serializers=[
                    BrandedFoodItemSerializer,
                    FoundationFoodItemSerializer,
                    AbridgedFoodItemSerializer,
                ],
                resource_type_field_name="dataType",
            ),
        }
    )
    def get(self, request, fdc_ids: str):
        res = fdc_client.get_food(fdc_ids=fdc_ids.split(","), format="full")
        return Response(res.json(), status=status.HTTP_200_OK)


class UserFoodPreferenceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: UserFoodPreferenceSerializer, 403: ErrorSerializer})
    def get(self, request):
        preferences = UserFoodPreference.objects.filter(user=request.user)
        return Response(UserFoodPreferenceSerializer(preferences), status=status.HTTP_200_OK)

    @extend_schema(
        request=UserFoodPreferencesDTOSerializer,
        responses={200: UserFoodPreferenceSerializer, 403: ErrorSerializer},
    )
    def post(self, request):
        preferenceDTO = UserFoodPreferencesDTOSerializer(request.data).validate()
        preference = UserFoodPreference.objects.get(fdc_id=preferenceDTO.validated_data.fdc_id)
        preference.dislikes = preferenceDTO.validated_data.dislikes
        preference.save()
        return Response(UserFoodPreferenceSerializer(preference), status=status.HTTP_200_OK)
