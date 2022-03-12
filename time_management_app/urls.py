from django.urls import path
from time_management_app import views
from time_management_app.api.get_ratings import get_ratings

app_name = "time_management"

urlpatterns = [
    path("", views.Home.as_view(), name="index"),
    path("new/", views.New.as_view(), name="new"),
    path("detail/<int:id>/", views.Detail.as_view(), name="detail"),
    path("detail/<int:id>/edit/", views.Edit.as_view(), name="edit"),
    path("detail/<int:pk>/delete/", views.Delete.as_view(), name="delete"),
    path("download/<str:month>", views.file_download, name="download"),
    path("visualize/", views.Visualize.as_view(), name="visualize"),
    path("api/get_ratings/", get_ratings, name="get_ratings"),
]
