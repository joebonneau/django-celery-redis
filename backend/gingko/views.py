from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from gingko.models import Submission
from gingko.serializers import SubmissionSerializer


@api_view(["GET"])
def submissions_list(request):
    if request.method == "GET":
        submissions = Submission.objects.all()
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
