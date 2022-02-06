from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/random/", views.random_entry, name="random-page"),
    path("search/", views.search, name="search"),
    path("create/", views.create_new_page, name="create-new-page"),
]
