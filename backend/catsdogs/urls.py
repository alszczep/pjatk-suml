from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("predict", views.predict, name="predict"),
    path("all_predictions", views.all_predictions, name="all_predictions"),
    path(
        "change_vote_and_feedback",
        views.change_vote_and_feedback,
        name="change_vote_and_feedback",
    ),
]
