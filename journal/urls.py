from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.UserDashboardView.as_view()),
    path("entries/", views.UserFoodJournalEntriesView.as_view()),
    path("entries/create/", views.CreateUserFoodJournalEntryView.as_view()),
]
