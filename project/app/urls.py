from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    path("auth",views.signup,name="auth"),
    path("",views.home,name=""),
    path("event_info",views.event_info,name="event_info"),

    path("create_form/<str:file>/<int:pk>",views.create_form,name="create_form"),
    path("form/<int:pk>",views.form_render,name="form_render"),
    path("api/form/<int:pk>",views.formapi,name="api/form"),
    path("submit-form/<str:file>/<int:pk>",views.submit_form,name="submit-form"),
]