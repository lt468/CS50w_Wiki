from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    # Displays the contents of the markdown files for the wiki page
    path("wiki/<str:page>", views.page_render, name="content"),
    # Search page
    path("search", views.search_page, name="search"),
    # New page
    path("create", views.new_page, name="create"),
    # Already created page
    path("already_created/<str:title>", views.already_created, name="already_created"),
    # Edit page
    path("wiki/<str:page>/edit", views.editing_page, name="edit"),
    # Random page
    path("random", views.random_page, name="random")
]
