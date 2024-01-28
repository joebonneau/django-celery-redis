from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import submissions_list, results_list


urlpatterns = [
    path("results/", results_list),
    path("submissions/", submissions_list)
]
urlpatterns = format_suffix_patterns(urlpatterns)
