from django.urls import path
from newsapp.views import index

urlpatterns = [
    path("", index, name="index")
]

app_name = "newsapp"
