from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import submissions_list, results_list


urlpatterns = [
    path("results/", submissions_list),
    path("submissions/", results_list),
]
urlpatterns = format_suffix_patterns(urlpatterns)
