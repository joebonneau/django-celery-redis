from django.db import models

# Create your models here.

class Result(models.Model):
    id = models.AutoField(primary_key=True)
    protein_name = models.CharField(max_length=50)
    loc_in_protein_seq = models.IntegerField()

class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    initiated_on = models.DateTimeField()
    completed_on = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, default="pending")
    dna_sequence = models.CharField(max_length=100)
    result = models.ForeignKey("Result", on_delete=models.PROTECT, blank=True, null=True)

