from django.urls import path
from . import views

app_name = "downloader"

urlpatterns = [
    path('', views.index, name = "index")
]