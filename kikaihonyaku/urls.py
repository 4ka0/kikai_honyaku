from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.translate, name="input"),
    path("output/", views.translate, name="output"),
]
