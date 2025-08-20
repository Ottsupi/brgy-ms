from django.urls import path

from . import views

app_name = "app"

urlpatterns = [
    path("health_check", views.health_check, name="health_check"),
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
