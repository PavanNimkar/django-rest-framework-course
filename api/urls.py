from django.urls import path
from home import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path("person/", views.person, name="person"),
]
