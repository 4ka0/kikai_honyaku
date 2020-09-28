from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.translate, name="home"),
    path("translate/", views.translate, name="translate"),
]
