from django.urls import path

from . import views

app_name = "document"

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create_view, name="create"),
    path("request", views.request_list_view, name="request_list"),
    path("issuable", views.issuable_document_list_view, name="issuable_document_list"),
]
