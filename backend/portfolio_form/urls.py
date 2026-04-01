from django.urls import path
from . import views

urlpatterns = [
    path("submit_form/", views.submitForm, name="submitForm"),
]