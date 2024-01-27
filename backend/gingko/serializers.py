from rest_framework import serializers

from gingko.models import Result, Submission

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ("initiated_on", "completed_on", "status", "result")

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ("protein_name", "loc_in_protein_seq")
