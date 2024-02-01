from rest_framework import serializers

from gingko.models import Result, Submission


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ("id", "genome_name", "start_index", "end_index", "match_found")


class SubmissionSerializer(serializers.ModelSerializer):
    result = ResultSerializer(read_only=True, required=False)

    class Meta:
        model = Submission
        fields = (
            "id",
            "initiated_on",
            "completed_on",
            "dna_sequence",
            "status",
            "result",
        )
