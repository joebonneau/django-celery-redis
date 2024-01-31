from datetime import datetime

from asgiref.sync import async_to_sync
from Bio import Entrez, SeqIO
from celery import shared_task
from channels.layers import get_channel_layer
from django.forms.models import model_to_dict

from gingko.models import Result, Submission
from gingko.serializers import SubmissionSerializer

GENOMES = [
    "NC_000852", 
    "NC_007346", 
    "NC_008724", 
    "NC_009899", 
    "NC_014637", 
    "NC_020104",  
    "NC_023423", 
    "NC_023640", 
    "NC_023719",
    "NC_027867"
]

def fetch_genome_record(genome):
    Entrez.email = "joebonneau@gmail.com"

    handle = Entrez.efetch(db="nucleotide", id=genome, rettype="gb", retmode="text")
    record = SeqIO.read(handle, "genbank")
    handle.close()

    return record

@shared_task
def align_sequences(submission_id, dna_sequence):
    submission_obj = Submission.objects.get(id=submission_id)
    start = None
    for genome in GENOMES:
        genome_record = fetch_genome_record(genome)
        idx = genome_record.seq.find(dna_sequence)
        if idx != -1:
            start = idx
            break
    result_obj = None
    if start is not None:
        result_obj = Result.objects.create(protein_name=genome, loc_in_protein_seq=start)
        submission_obj.result = result_obj
    submission_obj.status = "completed"
    submission_obj.completed_on = datetime.now()
    submission_obj.save()
    # FIXME: this is stupid logic, get rid of serializer... model_to_dict probably doesn't capture the result field
    submission_serializer = SubmissionSerializer(data=model_to_dict(submission_obj))
    if not submission_serializer.is_valid():
        return 
    else:
        submission_obj.status = "completed"
        submission_obj.completed_on = datetime.now()
        submission_obj.save()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "tasks",
        {
            "type": "task.complete",
            "submission_id": submission_id,
            "result_id": result_obj.id if result_obj else result_obj,
            **dict(submission_serializer.data),
        },
    )
