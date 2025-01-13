from django.urls import path

from . import views

app_name = "review"

urlpatterns = [
    path("add/", views.add_review, name="add_review"),
    # path("error/", views.Error.as_view(), name="error"),

]
