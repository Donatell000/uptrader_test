from django.urls import path

from . import views


app_name = "menu"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("<slug:slug>/", views.page_view, name="page"),
]
