from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import submissions_list

urlpatterns = [path("submissions/", submissions_list)]
urlpatterns = format_suffix_patterns(urlpatterns)
