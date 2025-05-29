from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "core"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="logout.html"),
        name="logout",
    ),
    
    path('dash_siswa/', views.dash_siswa, name='siswa/dash_siswa.html'),
    path('exam/<int:exam_id>/', views.exam_view, name='exam_view'),
    path('save_answer/', views.save_answer, name='save_answer'),
    path('submit_exam/', views.submit_exam, name='submit_exam'),
    path('exam_result/<int:exam_id>/', views.exam_result, name='exam_result'),
    path('mark_review/', views.mark_review, name='mark_review'),
]   


    
