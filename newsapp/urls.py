from django.urls import path
from newsapp.views import (
    index,
    TopicListView,
    NewspaperListView,
    NewspaperDetailView,
    RedactorListView,
    RedactorDetailView,
)

urlpatterns = [
    path("", index, name="index"),
    path("topic/", TopicListView.as_view(), name="topic-list"),
    path("newspaper/", NewspaperListView.as_view(), name="newspaper-list"),
    path("newspaper/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("newspaper/", RedactorListView.as_view(), name="redactor-list"),
    path("newspaper/<int:pk>/", RedactorDetailView.as_view(), name="redactor-detail"),
]

app_name = "newsapp"
