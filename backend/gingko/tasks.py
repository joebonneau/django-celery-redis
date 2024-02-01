from datetime import datetime

from asgiref.sync import async_to_sync
from Bio import Entrez, SeqIO
from celery import shared_task
from channels.layers import get_channel_layer
from django.forms.models import model_to_dict

from gingko.models import Result, Submission

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
    "NC_027867",
]


def fetch_genome_record(genome):
    Entrez.email = "joebonneau@gmail.com"
    # This will throw an IOError if the network can't be reached and terminate the task
    handle = Entrez.efetch(db="nucleotide", id=genome, rettype="gb", retmode="text")
    record = SeqIO.read(handle, "genbank")
    handle.close()

    return record


@shared_task
def align_sequences(submission_id, dna_sequence):
    start = None
    genome_name = ""
    idx = -1
    for genome in GENOMES:
        genome_record = fetch_genome_record(genome)
        idx = genome_record.seq.find(dna_sequence)
        if idx != -1:
            start = idx
            genome_name = genome
            break
    result_obj = Result.objects.create(
        genome_name=genome_name if start else None,
        start_index=start,
        end_index=start + len(dna_sequence) if start is not None else None,
        match_found=idx != -1,
    )
    new_data = {
        "result": result_obj,
        "status": "completed",
        "completed_on": datetime.now(),
    }
    Submission.objects.filter(id=submission_id).update(**new_data)
    # FIXME: I would love to know why the serializers are failing me here. This seems
    # like a stupid way to have to do this.
    submission_obj = Submission.objects.get(id=submission_id)
    result_obj = Result.objects.get(id=result_obj.id)
    submission_dict = model_to_dict(
        submission_obj, fields=[field.name for field in submission_obj._meta.fields]
    )
    submission_dict["initiated_on"] = submission_dict["initiated_on"].isoformat()
    submission_dict["completed_on"] = submission_dict["completed_on"].isoformat()
    result_dict = model_to_dict(
        result_obj, fields=[field.name for field in result_obj._meta.fields]
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "tasks",
        {
            "type": "task.complete",
            **{**submission_dict, "result": result_dict},
        },
    )
