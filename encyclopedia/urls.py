from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("wiki/<str:title>", views.getEntry, name = "getEntry"),
    path("search", views.search, name = "search"),
    path("create", views.create, name = "create"),
    path("edit", views.edit, name = "edit"),
    path("save", views.save, name = "save"),
    path("random_entry", views.random_entry, name = "random_entry"),
]
