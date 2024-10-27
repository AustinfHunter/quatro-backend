from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import UserFoodJournalEntry


class IsJournalEntryOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        entry: UserFoodJournalEntry = get_object_or_404(
            UserFoodJournalEntry, id=view.kwargs.get("id", None)
        )
        return entry.user == request.user
