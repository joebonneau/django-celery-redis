from Bio import Entrez, SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

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

def fetch_protein(protein_accession):
    # Fetch the protein record
    handle = Entrez.efetch(db="protein", id=protein_accession, rettype="gb", retmode="text")
    record = SeqIO.read(handle, "genbank")
    handle.close()

    return record

def fetch_genome(genome):
    Entrez.email = "joebonneau@gmail.com"

    # Fetch the genome record
    handle = Entrez.efetch(db="nucleotide", id=genome, rettype="gb", retmode="text")
    genome_record = SeqIO.read(handle, "genbank")
    handle.close()

    protein_accessions = []

    # Extract protein accessions from features in the genome record
    for feature in genome_record.features:
        if feature.type == "CDS" and "protein_id" in feature.qualifiers:
            protein_accessions.extend(feature.qualifiers["protein_id"])

    # Fetch protein records for each protein accession
    protein_records = []
    for protein_accession in protein_accessions:
        protein_records.append(fetch_protein(protein_accession))

    return protein_records, genome_record

if __name__ == "__main__":
    for genome in GENOMES:
        sequence = "CTTTTCTCTCGAGCGGAGGGAAAACGGAA"
        # sequence = "CCCCCCCCAAAAAAAGGGGGGAAAAAATTTTTTTTTTTTT"
        # seq_obj = fetch_genome(genome)
        protein_records, genome_record = fetch_genome(genome)
        record = SeqRecord(genome_record.seq, id=genome)
        idx = record.seq.find(sequence)
        if idx != -1:
            print(genome, idx, idx + len(sequence))
            start = idx
            end = idx + len(sequence)
            found_seq = Seq(str(record.seq[start:end]))
            translated_seq = found_seq.translate()
            for record in protein_records:
                if translated_seq in record.seq:
                    print(record.id)
                    break
        else:
            print("not found")

