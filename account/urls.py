from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "account"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout_view"),
    # siswa
    path("siswa/dashboard/", views.siswa_dashboard, name="siswa_dashboard"),
    path("siswa/settings/", views.user_profile, name="user_profile"),
    # guru
    path("guru/dashboard/", views.guru_dashboard, name="guru_dashboard"),
    path("guru/settings/", views.user_profile, name="user_profile"),
]
