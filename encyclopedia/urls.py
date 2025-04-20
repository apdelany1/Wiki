from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("easteregg/", views.easteregg, name="easteregg"),
    path("search/", views.search, name="search"),
    path("wiki/<str:name>", views.page, name="entry"),
    path("add/", views.add, name="add"),
    path("edit/", views.edit, name="edit"),
    path("saveEdit/", views.saveEdit, name="saveEdit"),
    path("randomPage/", views.randomPage, name="randomPage")
]