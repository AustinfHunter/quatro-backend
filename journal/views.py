from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response
from rest_framework import status, permissions
from .serializers import (
    UserFoodJournalEntryDTOSerializer,
    UserFoodJournalEntrySerializer,
    EntriesRequestSerializer,
    UserFoodJournalEntryListSerializer,
    UserDashboardSerializer,
    EntryTrendDataSerializer,
)
from .models import UserFoodJournalEntry
from .permissions import IsJournalEntryOwner
from foods.util import get_or_create_food
from foods.serializers import ResponseDetailSerializer
from drf_spectacular.utils import extend_schema
from .util import getNutrientAmountOrZero


class UserFoodJournalEntriesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=EntriesRequestSerializer,
        responses={
            200: UserFoodJournalEntryListSerializer,
            400: ResponseDetailSerializer,
        },
    )
    def get(self, request):
        serializer = EntriesRequestSerializer(data=request.data)
        if serializer.is_valid():
            entries = UserFoodJournalEntry.objects.filter(
                date=serializer.validated_data.get("date")
            )
            return Response(
                UserFoodJournalEntryListSerializer({"journal_entries": entries}).data,
                status=status.HTTP_200_OK,
            )
        return Response(
            ResponseDetailSerializer({"detail": "Could not get journal entries"}).data,
            status=status.HTTP_400_BAD_REQUEST,
        )


class CreateUserFoodJournalEntryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=UserFoodJournalEntryDTOSerializer,
        responses={
            200: UserFoodJournalEntrySerializer,
        },
    )
    def post(self, request):
        serializer = UserFoodJournalEntryDTOSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            food = get_or_create_food(serializer.validated_data["fdc_id"])
            date = serializer.validated_data.get("date", timezone.now().date())
            amount_consumed = serializer.validated_data["amount_consumed_grams"]
            result = UserFoodJournalEntry(
                user=user, food=food, date=date, amount_consumed_grams=amount_consumed
            )
            result.save()
            return Response(
                UserFoodJournalEntrySerializer(result).data, status=status.HTTP_201_CREATED
            )
        else:
            print(serializer.errors)
        return Response(
            ResponseDetailSerializer({"detail": "Could not create journal entry"}).data,
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserFoodJournalEntryView(APIView):
    permission_classes = [permissions.IsAuthenticated & IsJournalEntryOwner]

    @extend_schema(
        responses={
            200: UserFoodJournalEntrySerializer,
            403: ResponseDetailSerializer,
            404: ResponseDetailSerializer,
        }
    )
    def get(self, request, id):
        entry = get_object_or_404(UserFoodJournalEntry, id=id)
        return Response(UserFoodJournalEntrySerializer(entry).data)

    @extend_schema(
        request=UserFoodJournalEntryDTOSerializer,
        responses={
            202: UserFoodJournalEntrySerializer,
            400: ResponseDetailSerializer,
            403: ResponseDetailSerializer,
        },
    )
    def put(self, request, id):
        serializer = UserFoodJournalEntryDTOSerializer(data=request.data)
        if serializer.is_valid():
            entry: UserFoodJournalEntry = get_object_or_404(
                UserFoodJournalEntry,
                id=id,
                date=serializer.validated_data.get("date", timezone.now().date()),
            )
            entry.amount_consumed_grams = serializer.validated_data.get("amount_consumed_grams")
            entry.save()
            return Response(
                UserFoodJournalEntrySerializer(entry).data, status=status.HTTP_202_ACCEPTED
            )
        return Response(
            ResponseDetailSerializer({"detail": "Could not update journal entry"}).data,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        responses={
            202: ResponseDetailSerializer,
            403: ResponseDetailSerializer,
            404: ResponseDetailSerializer,
        }
    )
    def delete(self, request, id):
        entry = get_object_or_404(UserFoodJournalEntry, id=id)
        entry.delete()
        return Response(
            ResponseDetailSerializer({"detail": "Successfully deleted journal entry"}).data,
            status=status.HTTP_202_ACCEPTED,
        )


class UserDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={
            200: UserDashboardSerializer,
        }
    )
    def get(self, request):
        entries = UserFoodJournalEntry.objects.filter(date=timezone.now().date(), user=request.user)
        return Response(
            UserDashboardSerializer(
                {"journal_entries": entries},
                context={"user": request.user, "date": timezone.now()},
            ).data,
            status=status.HTTP_200_OK,
        )


class HistoricalUserDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: UserDashboardView})
    def get(self, request, date):
        entries = UserFoodJournalEntry.objects.filter(date=date, user=request.user)
        return Response(
            UserDashboardSerializer(
                {"journal_entries": entries},
                context={"user": request.user, "date": date},
            ).data,
            status=status.HTTP_200_OK,
        )


class UserJournalEntryTrendView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: EntryTrendDataSerializer(many=True), 401: ResponseDetailSerializer}
    )
    def get(self, request, start_date):
        result = {}
        entries = UserFoodJournalEntry.objects.filter(
            user=request.user, date__range=(start_date, timezone.now().today())
        )
        for entry in entries:
            calories = getNutrientAmountOrZero(entry.food.food_nutrients, nutrient_name="Energy")
            if entry.date in result:
                result[entry.date]["calories"] += (calories / 100) * entry.amount_consumed_grams
            else:
                result[entry.date] = {
                    "date": entry.date,
                    "calories": (calories / 100) * entry.amount_consumed_grams,
                }
        return Response(
            EntryTrendDataSerializer(result.values(), many=True).data, status=status.HTTP_200_OK
        )
