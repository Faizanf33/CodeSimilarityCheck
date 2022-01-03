
from os import name
from django.urls import path
from csc import views
urlpatterns = [
    path("", views.dashboard, name="csc"),
    path("about", views.about, name="about"),
    path("history", views.history, name="history"),
    path("multiple", views.upload_multiple_files, name="multiple")
]
