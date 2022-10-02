from django.urls import re_path

from public_website.views import pre_launch_view

urlpatterns = [
    re_path(".*", pre_launch_view, name="pre_launch"),
]
