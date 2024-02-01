from django.db import models


class Result(models.Model):
    id = models.AutoField(primary_key=True)
    genome_name = models.CharField(max_length=50, null=True)
    start_index = models.IntegerField(null=True)
    end_index = models.IntegerField(null=True)
    match_found = models.BooleanField(default=False)


class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    initiated_on = models.DateTimeField()
    completed_on = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, default="pending")
    dna_sequence = models.CharField(max_length=100)
    result = models.ForeignKey(
        "Result", on_delete=models.PROTECT, blank=True, null=True
    )
