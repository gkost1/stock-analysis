from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("auth/register/", views.RegisterView.as_view(), name="register"),
    path("auth/login/", views.LoginView.as_view(), name="login"),
    path("auth/logout/", views.LogoutView.as_view(), name="logout"),
    path("testing/seed/", views.SeedView.as_view(), name="testing-seed"),
]
