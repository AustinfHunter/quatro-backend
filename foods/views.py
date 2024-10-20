from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.exceptions import APIException
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
    UserFoodPreferenceListSerializer,
    UserFoodRestrictionListSerializer,
    ResponseDetailSerializer,
)
from django.shortcuts import get_object_or_404


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

    @extend_schema(
        request=UserFoodPreferencesDTOSerializer,
        responses={
            200: UserFoodPreferenceSerializer,
            400: ResponseDetailSerializer,
            403: ResponseDetailSerializer,
        },
    )
    def put(sel, request, fdc_id):
        pref = get_object_or_404(UserFoodPreference, user=request.user, fdc_id=fdc_id)
        serializer = UserFoodPreferenceSerializer(pref, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(
            ResponseDetailSerializer({"detail": "Failed to update preference."}).data,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        responses={
            202: ResponseDetailSerializer,
            403: ResponseDetailSerializer,
            404: ResponseDetailSerializer,
        }
    )
    def delete(self, request, fdc_id):
        preference = UserFoodPreference.objects.get(user=request.user, fdc_id=fdc_id)
        preference.delete()
        return Response(
            ResponseDetailSerializer({"detail": "Successfully deleted preference"}),
            status=status.HTTP_202_ACCEPTED,
        )


class CreateUserFoodPreferenceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=UserFoodPreferencesDTOSerializer,
        responses={
            201: UserFoodPreferenceSerializer,
            403: ResponseDetailSerializer,
            400: ResponseDetailSerializer,
        },
    )
    def post(self, request):
        prefDTO = UserFoodPreferencesDTOSerializer(data=request.data, context={"request": request})
        if prefDTO.is_valid():
            exists = UserFoodPreference.objects.filter(
                user=request.user, fdc_id=prefDTO.validated_data["fdc_id"]
            ).exists()

            if exists:
                return Response(
                    ResponseDetailSerializer({"message": "Preference already exists"}).data,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            result = prefDTO.save()
            return Response(
                UserFoodPreferenceSerializer(result).data, status=status.HTTP_201_CREATED
            )
        return Response(
            ResponseDetailSerializer({"detail": "Failed to create preference"}).data,
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserFoodPreferencesListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: UserFoodPreferenceListSerializer, 403: ResponseDetailSerializer})
    def get(self, request):
        preferences = UserFoodPreference.objects.filter(user=request.user)
        return Response(
            UserFoodPreferenceListSerializer({"preferences": preferences}).data,
            status=status.HTTP_200_OK,
        )


class UserFoodRestrictionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=UserFoodRestrictionDTOSerializer,
        responses={
            200: UserFoodRestrictionSerializer,
            400: ResponseDetailSerializer,
            403: ResponseDetailSerializer,
        },
    )
    def put(sel, request, fdc_id):
        restriction = get_object_or_404(UserFoodRestriction, user=request.user, fdc_id=fdc_id)
        serializer = UserFoodRestrictionSerializer(restriction, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(
            ResponseDetailSerializer({"detail": "Failed to update preference."}).data,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(responses={202: ResponseDetailSerializer, 404: ResponseDetailSerializer})
    def delete(self, request, fdc_id):
        restriction = get_object_or_404(UserFoodRestriction, user=request.user, fdc_id=fdc_id)
        restriction.delete()
        return Response(
            ResponseDetailSerializer({"detail": "Successfully deleted preference"}).data,
            status=status.HTTP_202_ACCEPTED,
        )


class CreateUserFoodRestrictionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=UserFoodRestrictionDTOSerializer,
        responses={
            201: UserFoodRestrictionSerializer,
            403: ResponseDetailSerializer,
            400: ResponseDetailSerializer,
        },
    )
    def post(self, request):
        prefDTO = UserFoodRestrictionDTOSerializer(data=request.data, context={"request": request})
        if prefDTO.is_valid():
            exists = UserFoodRestriction.objects.filter(
                user=request.user, fdc_id=prefDTO.validated_data["fdc_id"]
            ).exists()

            if exists:
                return Response(
                    ResponseDetailSerializer({"detail": "Preference already exists"}).data,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            result = prefDTO.save()
            return Response(
                UserFoodRestrictionSerializer(result).data, status=status.HTTP_201_CREATED
            )
        return Response(
            ResponseDetailSerializer({"detail": "Failed to create preference"}).data,
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserFoodRestrictionListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: UserFoodRestrictionListSerializer, 403: ResponseDetailSerializer}
    )
    def get(self, request):
        restrictions = UserFoodRestriction.objects.filter(user=request.user)
        return Response(
            UserFoodPreferenceListSerializer({"restrictions": restrictions}).data,
            status=status.HTTP_200_OK,
        )
