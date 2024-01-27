from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from gingko.models import Result, Submission
from gingko.serializers import ResultSerializer, SubmissionSerializer


@api_view(["GET", "POST"])
def submissions_list(request):
    if request.method == "GET":
        submissions = Submission.objects.all()
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = SubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "POST"])
def results_list(request):
    if request.method == "GET":
        results = Result.objects.all()
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
