from django.urls import path
from newsapp.views import (
    index,
    TopicListView,
    TopicCreateView,
    TopicUpdateView,
    TopicDeleteView,
    NewspaperListView,
    NewspaperDetailView,
    RedactorListView,
    RedactorDetailView,
)

urlpatterns = [
    path("", index, name="index"),
    path("topic/", TopicListView.as_view(), name="topic-list"),
    path("topic/create/", TopicCreateView.as_view(), name="topic-create"),
    path("topic/<int:pk>/update/", TopicUpdateView.as_view(), name="topic-update"),
    path("topic/<int:pk>/delete/", TopicDeleteView.as_view(), name="topic-delete"),
    path("newspaper/", NewspaperListView.as_view(), name="newspaper-list"),
    path("newspaper/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("redactor/", RedactorListView.as_view(), name="redactor-list"),
    path("redactor/<int:pk>/", RedactorDetailView.as_view(), name="redactor-detail"),
]

app_name = "newsapp"
