from django.urls import path
from rest_framework.authtoken import views as authtoken_views
from . import views

urlpatterns = [
    path("login/", authtoken_views.obtain_auth_token),
    path("signup/", views.SignUpView.as_view()),
    path("account/<uuid:id>", views.AccountView.as_view()),
]
