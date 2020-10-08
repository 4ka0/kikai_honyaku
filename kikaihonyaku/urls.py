from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.translate, name="redirect_root_url"),
    path("input/", views.translate, name="input"),
    path("output/", views.translate, name="output"),
]
