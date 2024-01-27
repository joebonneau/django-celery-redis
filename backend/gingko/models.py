from django.db import models

# Create your models here.

class Result(models.Model):
    protein_name = models.CharField(max_length=50)
    loc_in_protein_seq = models.IntegerField()
    submission_id = models.ForeignKey("Submission", on_delete=models.PROTECT)

class Submission(models.Model):
    initiated_on = models.DateTimeField()
    completed_on = models.DateTimeField()
    status = models.CharField(max_length=20)
    result = models.OneToOneField(
        "Result",
        on_delete=models.PROTECT,
    )


