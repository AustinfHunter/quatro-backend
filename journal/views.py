from django.utils import timezone
from rest_framework.views import APIView, Response
from rest_framework import status
from .serializers import (
    UserFoodJournalEntryDTOSerializer,
    UserFoodJournalEntrySerializer,
    UserFoodJournalEntryListSerializer,
    UserDashboardSerializer,
)
from .models import UserFoodJournalEntry
from foods.util import get_or_create_food
from foods.serializers import ResponseDetailSerializer
from drf_spectacular.utils import extend_schema


class UserFoodJournalEntriesView(APIView):
    @extend_schema(
        responses={
            200: UserFoodJournalEntryListSerializer,
        }
    )
    def get(self, request):
        entries = UserFoodJournalEntry.objects.filter(date=timezone.now().date())
        return Response(
            UserFoodJournalEntryListSerializer({"journal_entries": entries}),
            status=status.HTTP_200_OK,
        )


class CreateUserFoodJournalEntryView(APIView):
    @extend_schema(
        request=UserFoodJournalEntryDTOSerializer,
        responses={
            200: UserFoodJournalEntrySerializer,
        }
    )
    def post(self, request):
        serializer = UserFoodJournalEntryDTOSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            food = get_or_create_food(serializer.validated_data["fdc_id"])
            date = timezone.now().date()
            amount_consumed = serializer.validated_data["amount_consumed_grams"]
            response = UserFoodJournalEntrySerializer(
                {
                    "user": user,
                    "food": food,
                    "date": date,
                    "amount_consumed_grams": amount_consumed,
                }
            )
            response.save()
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(
            ResponseDetailSerializer({"detail": "Could not create journal entry"}),
            status=status.HTTP_400_BAD_REQUEST,
        )


class ModifyUserFoodJournalEntryView(APIView):
    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass


class UserDashboardView(APIView):
    @extend_schema(
        responses={
            200: UserDashboardSerializer,
        }
    )
    def get(self, request):
        entries = UserFoodJournalEntry.objects.filter(date=timezone.now().date())
        return Response(
            UserDashboardSerializer({"journal_entries": entries}), status=status.HTTP_200_OK
        )
