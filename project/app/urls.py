from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    path("auth",views.auth,name="auth"),
    path("",views.home,name=""),
    path("event_info",views.event_info,name="event_info"),
    path("create_form/<str:file>/<int:pk>",views.create_form,name="create_form"),
    path("submit-form/<str:file>/<int:pk>",views.submit_form,name="submit-form"),
    path("api/form-structure/<str:url>",views.event_form,name="event"),
]