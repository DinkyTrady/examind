from django.urls import path

from . import views

app_name = "homeweb"

urlpatterns = [
    path("", views.index, name="index"),
    path("aboutus", views.aboutus, name="about_us"),
]
