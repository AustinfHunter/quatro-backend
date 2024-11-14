from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.UserDashboardView.as_view()),
    path("dashboard/<str:date>/", views.HistoricalUserDashboardView.as_view()),
    path("entry/<int:id>", views.UserFoodJournalEntryView.as_view()),
    path("entries/", views.UserFoodJournalEntriesView.as_view()),
    path("entries/create/", views.CreateUserFoodJournalEntryView.as_view()),
    path("data/trend/<str:start_date>", views.UserJournalEntryTrendView.as_view()),
]
