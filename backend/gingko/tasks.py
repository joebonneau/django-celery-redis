from celery import shared_task
import time
from gingko.serializers import ResultSerializer
from gingko.models import Submission

# TODO: Add celery task that implements the Biopython alignment algorithm

@shared_task
def align_sequences(submission_id):
    time.sleep(10)
    serializer = ResultSerializer(data={"protein_name": "test", "loc_in_protein_seq": 1})
    if serializer.is_valid():
        result_obj = serializer.save()
        submission_obj = Submission.objects.get(id=submission_id)
        submission_obj.result = result_obj
        submission_obj.status = "completed"
        submission_obj.save()
