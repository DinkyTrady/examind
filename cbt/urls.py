from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "cbt"

urlpatterns = [
    path("exam/<int:exam_id>/", views.exam_view, name="exam_view"),
    path("exam/save/", views.save_answer, name="save_answer"),
    path("exam/submit/", views.submit_exam, name="submit_exam"),
    path("exam/result/<int:exam_id>/", views.exam_result, name="exam_result"),
    path("exam/review/", views.mark_review, name="mark_review"),
]

