from django.urls import path

from . import views

urlpatterns = [path("", views.WindowView.as_view(), name="index")]
