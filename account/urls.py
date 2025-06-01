from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "account"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout_view"),
    # siswa
    path("siswa/dashboard/", views.siswa_dashboard, name="siswa_dashboard"),
    path("siswa/settings/", views.user_profile, name="siswa_profile"),
    # guru
    path("guru/dashboard/", views.guru_dashboard, name="guru_dashboard"),
    path("guru/settings/", views.user_profile, name="guru_profile"),
    # guru exam management
    path("guru/exams/", views.guru_exam_list, name="guru_exam_list"),
    path("guru/exams/create/", views.guru_exam_create, name="guru_exam_create"),
    path("guru/exams/<int:exam_id>/", views.guru_exam_detail, name="guru_exam_detail"),
    path("guru/exams/<int:exam_id>/edit/", views.guru_exam_edit, name="guru_exam_edit"),
    path(
        "guru/exams/<int:exam_id>/delete/",
        views.guru_exam_delete,
        name="guru_exam_delete",
    ),
    path(
        "guru/exams/<int:exam_id>/questions/create/",
        views.guru_question_create,
        name="guru_question_create",
    ),
    path(
        "guru/questions/<int:question_id>/edit/",
        views.guru_question_edit,
        name="guru_question_edit",
    ),
    path(
        "guru/questions/<int:question_id>/delete/",
        views.guru_question_delete,
        name="guru_question_delete",
    ),
]
