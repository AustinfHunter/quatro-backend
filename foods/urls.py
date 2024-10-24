from django.urls import path
from . import views

urlpatterns = [
    path("<str:fdc_ids>", views.GetFoodsView.as_view()),
    path("preferences/", views.UserFoodPreferencesListView.as_view()),
    path("preferences/<int:fdc_id>", views.UserFoodPreferenceView.as_view()),
    path("preferences/create/", views.CreateUserFoodPreferenceView.as_view()),
    path("restrictions/", views.UserFoodRestrictionListView.as_view()),
    path("restrictions/<int:fdc_id>", views.UserFoodRestrictionView.as_view()),
    path("restrictions/create/", views.CreateUserFoodRestrictionView.as_view()),
    path("search/<str:query>", views.FoodSearchView.as_view()),
]
