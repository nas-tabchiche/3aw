from django.urls import re_path

from .views import TestProxyView

urlpatterns = [
    re_path(r"(?P<path>.*)", TestProxyView.as_view()),
]
