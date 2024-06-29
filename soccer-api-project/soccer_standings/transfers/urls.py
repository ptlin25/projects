from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("league/<int:pk>", views.team_list, name="team-list")
]