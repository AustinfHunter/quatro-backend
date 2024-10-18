from django.urls import path
from . import views

urlpatterns = [
    path("<str:fdc_ids>", views.GetFoodsView.as_view()),
    path("preferences/", views.UserFoodPreferenceView.as_view()),
]
