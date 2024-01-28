from rest_framework import serializers

from gingko.models import Result, Submission


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ("id", "protein_name", "loc_in_protein_seq")


class SubmissionSerializer(serializers.ModelSerializer):
    result = ResultSerializer()
    class Meta:
        model = Submission
        fields = ("id", "initiated_on", "completed_on", "status", "result")

