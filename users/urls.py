from django.urls import path
from rest_framework.authtoken import views as authtoken_views
from . import views

urlpatterns = [
    path("login/", authtoken_views.obtain_auth_token),
    path("signup/", views.SignUpView.as_view()),
    path("account/", views.AccountView.as_view()),
    path("fitness-profile/create/", views.CreateFitnessProfileView.as_view()),
    path("fitness-profile/", views.FitnessProfileView.as_view()),
]
