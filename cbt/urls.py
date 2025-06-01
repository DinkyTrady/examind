from django.urls import path
from . import views

app_name = "cbt"

urlpatterns = [
    path("exam/", views.exam_all, name="exam_all"),
    path("exam/<int:exam_id>/", views.exam_view, name="exam_view"),
    path("exam/<int:exam_id>/submit/", views.submit_exam, name="submit_exam"),
    path("exam/<int:exam_id>/result/", views.exam_result, name="exam_result"),
    path("save-answer/", views.save_answer, name="save_answer"),
    path("mark-review/", views.mark_review, name="mark_review"),
]
