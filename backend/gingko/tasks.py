from celery import shared_task
from datetime import datetime
import time
from gingko.serializers import ResultSerializer, SubmissionSerializer
from gingko.models import Result, Submission
from django.forms.models import model_to_dict
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
        submission_obj.completed_on = datetime.now()
        submission_obj.save()
        submission_serializer = SubmissionSerializer(data=model_to_dict(submission_obj))
        if submission_serializer.is_valid():
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "tasks",
                {"type": "task.complete", "submission_id": submission_id, **dict(submission_serializer.data)}
            )
        else:
            print(submission_serializer.errors)
