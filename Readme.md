How it works
============

Basically, run `setup.sh` to clone tool repos and make software.

The `prep.sh`, `split.sh` and `merge+qualfilter.sh` scripts then do the work.
Prep just makes the `sabre` keyfile, with the awk script provided (`key2sabre.awk`).
Then split does the demux, and merge+qualfilter does what it says on the tin.

This all expects a folder heirarchy, tree output follows:

    .
    ├── key2sabre.awk
    ├── keys
    │   └── key.bd4.txt
    ├── merge+qualfilter.sh
    ├── prep.sh
    ├── Readme.md
    ├── reads
    │   ├── 1
    │   │   ├── 1_nobcd_R1.fq		# reads that couldn't be assigned to a barcode
    │   │   ├── 1_nobcd_R2.fq
    │   │   ├── AAAAGTT_1.fq 		# split to a barcode
    │   │   ├── AAAAGTT_2.fq 		# Ditto, but R2
    │   │   ├── AAAAGTT_singles.fq		# reads whose pair failed qc
    │   │   ├── (ditto for the rest of the barcodes)
    │   │   └── plate1.ilfq.gz  		# concatenated, trimmed whole plate
    │   ├── 2
    │   │   ├── (truncated, but per 1)
    │   ├── 3
    │   │   ├── (truncated, but per 1)
    │   ├── 4
    │   │   ├── (truncated, but per 1)
    │   ├── 6
    │   │   ├── (truncated, but per 1)
    │   └── orig
    │       ├── plate1_R1.fq.gz -> /home/data/Sample_Brachypodium_plate1/Brachypodium_plate1_NoIndex_L006_R1_001.fastq.gz
    │       ├── plate1_R2.fq.gz -> /home/data/Sample_Brachypodium_plate1/Brachypodium_plate1_NoIndex_L006_R2_001.fastq.gz
    │       ├── plate2_R1.fq.gz -> /home/data/Sample_Brachypodium_plate2/Brachypodium_plate2_NoIndex_L007_R1_001.fastq.gz
    │       ├── plate2_R2.fq.gz -> /home/data/Sample_Brachypodium_plate2/Brachypodium_plate2_NoIndex_L007_R2_001.fastq.gz
    │       ├── plate3_R1.fq.gz -> /home/data/Sample_Brachypodium_plate3/Brachypodium_plate3_NoIndex_L008_R1_001.fastq.gz
    │       ├── plate3_R2.fq.gz -> /home/data/Sample_Brachypodium_plate3/Brachypodium_plate3_NoIndex_L008_R2_001.fastq.gz
    │       ├── plate4_R1.fq.gz -> /home/data/Sample_Brachypodium_plate4/Brachy_04_NoIndex_L006_R1_001.fastq.gz
    │       ├── plate4_R2.fq.gz -> /home/data/Sample_Brachypodium_plate4/Brachy_04_NoIndex_L006_R2_001.fastq.gz
    │       ├── plate6_R1.fq.gz -> /home/data/Sample_Brachypodium_plate6/AU11_NoIndex_L007_R1_001.fastq.gz
    │       └── plate6_R2.fq.gz -> /home/data/Sample_Brachypodium_plate6/AU11_NoIndex_L007_R2_001.fastq.gz
    ├── sampleSheet2sabre.awk
    ├── setup.sh
    ├── split.sh
    └── tools
        ├── sabre
        ├── scythe
        ├── seqtkwithpatches
        └── sickle

