> **Announcement:** As of 2026June15, FAS2rDNA Web is now available. Access the portal here for FREE: [FAS2rDNA Web](https://fas2rdna.chordexbio.com/)

<img width="200" height="200" alt="FAS2rDNA logo" src="https://github.com/mahvin92/FAS2rDNA/blob/main/asset/FAS2rDNA%20logo/1.png"/>

# FAS2rDNA
FAS2rDNA solves the hassle of manually retrieving and formatting sequences from genome assemblies. It automatically reconstructs multi-FASTA files from genomic coordinates in batches, saving hours of work and enabling fast, scalable analysis of large genomic datasets. The pipeline is a lightweight, assembly‑aware reconstruction engine that converts genomic coordinates into FASTA sequences (see Figure 1). It supports short fragments (e.g., microRNAs) to large regions (e.g., genes, isoforms, loci) across multiple species and assemblies, using a simple tabular input format optimized for downstream analytics and machine learning workflows.

<img width="500" height="500" alt="FAS2rDNA workflow" src="https://github.com/mahvin92/FAS2rDNA/blob/main/asset/FAS2rDNA%20framework.png"/>

Figure 1. Illustration of FAS2rDNA workflow.

#### Links:

Read the protocol here: [Protocols.io](https://dx.doi.org/10.17504/protocols.io.rm7vzenqxvx1/v1)

Visit the official wesite here: [FAS2rDNA by ChordexBio](https://fas2rdna.chordexbio.com/)


### Purpose
FAS2rDNA is designed for users who work with coordinate‑based genomic annotations rather than raw FASTA files. The major advantage of this workflow is that, given a minimal text input containing sample identifiers (sample_id) and genomic locations (seq_loc), the system reconstructs strand‑correct DNA sequences directly from reference assemblies. It operates in batch (multiple experiments), multi-assembly (detects different assembly versions like hg17, hg18, hg19, hg38 in humans), multi-loci (can reconstruct sequence from different DNA locations), auotomated formatting (compile multi-FASTA-formatted results, ready for downstream analyses), and multi-species (supports assemblies from humans to yeast genomes) workflows, giving users the speed, scalability, confidence and convenience needed to analyze and perform experiments using large genomic data.

The project emphasizes reproducibility, assembly transparency, and scalability. By decoupling sequence reconstruction from annotation logic, FAS2rDNA fits naturally into bioinformatics pipelines, forensic genomics, transcriptomics, and ML‑driven sequence modeling.

---

### Features
- Minimal: Requires only the coordinates of the sequences for reconstruction
- Strand-aware: Automatically everse complementats sequences in the negative strand
- Context-aware: Performs automatic multi‑species and multi‑assembly reconstruction
- Light-weight: Data is in the form of tab-deliminted text file (.txt or .tsv) with minimal data (sample_id and seq_loc)
- FASTA-friendly: Headers are optimized for traceability
- Scalable: Supports large cohorts and high‑throughput workflows
- Interoperable: Compatible with ML, forensic, and functional genomics pipelines

---

### Use Cases
1. Variant‑centered sequence reconstruction: Reconstruct flanking regions around SNPs, indels, or STRs for downstream analysis or modeling.
2. Gene and isoform assembly: Aggregate multiple coordinate fragments to reconstruct genes, transcripts, or isoform‑specific regions.
3. Machine learning feature engineering: Generate consistent, assembly‑aware DNA inputs for models such as CNNs, transformers, or TIPs‑based encodings.
4. Forensic and population genomics: Reconstruct Y‑STRs, autosomal loci, or ancestry‑informative markers directly from coordinate tables.
5. Cross‑assembly validation: Compare equivalent loci across different genome builds (e.g., hg19 vs hg38).

---

### Workflows
##### a. Input parsing
1. Validates required columns (seq_loc and sample_id; the seq_id and description fields are required for building custom headers)
2. Parses seq_loc into:
- Assembly version & type
- Chromosome number
- DNA location start / end coordinates
- Strand orientation or location

##### b. Assembly resolution
Determines which reference genome to load based on assembly required (version/type/species)

##### c. Sequence retrieval
Extracts genomic subsequences with strand-aware logic (+: direct extraction from reference | -: reverse complement)

##### d. FASATA reconstruction
Builds FASTA entries using:
- Header: sample_id (default)
- Sequence: reconstructed DNA fragment

##### e. Output
Writes reconstructed sequences to multi-FASTA files

---

### Usage
### 1. Preparing your data
#### a. Data format:
i) Required data columns:
- sample_id: the identifier of your sample (e.g., sample source)
- seq_loc: the genomic coordinate of your sequence (see below for standards)
- seq_id: the identifier of the sequence (e.g., gene name)
- description: any information about the sequence entry

Table 1. Sample data format.
| sample_id | seq_loc | seq_id | description |
| :--- | :--- | :--- | :--- |
| BLOOD_001 | hg19:9:106938220-106938244:+ | TP53 | Tumor protein p53; genomic locus on chromosome 17. |
| LIVER_A2 | hg38:11:86938550-86938664:- | BRCA2 | DNA repair protein; captured via targeted enrichment. |
| SKIN_NS | hg18:7:96998253-97038145:+ | BRAF | Proto-oncogene; wild-type sequence from control group. |
| BONE_M | hg19:1:76938211-76949381:- | NRAS | Neuroblastoma RAS viral oncogene homolog. |

*You can have additional headers as long as you have all the required columns*

ii) Use a tab-delimited text file (.txt or .tsv)

#### b. Standard genomic coordinate:
The *seq_loc* field MUST assume ONLY the following format: ```genome_assembly:chromosome_number:DNA_location:strand_location```, as shown in the Figure 1 below:. For example, the coordinate 'hg19:9:106938220-106938244:+' (as exemplified in Table 1) is to be reconstructed using the hg19 genome assembly, chromosome 9, DNA locations 106938220-106938244 nt, in the positive sense strand.

<img width="500" height="345" alt="FAS2rDNA coordinate" src="https://github.com/user-attachments/assets/bb80b03c-2703-4c8b-a6f0-f6c0a847af47" />

*Figure 1. Standard format for the genomic coordinate in the column seq_loc of your data.*


### 2. Performing a multi-FASTA reconstruction
i) Install dependencies

a. Get the required libraries or packages
```
pip install pandas pyfaidx tqdm
apt-get update -qq
apt-get install -y samtools
```

b. Get the cli version of fas2rdna_cli.py script that works for your OS
- Linux OS
``` /cli/cli-Lx/fas2rdna_cli.py```
- Non-Linux (MacOS, Windows)
```/cli/cli-NLx/fas2rdna_cli.py```


ii) Run FAS2rDNA, specifying the folder path that contains your input file/s and optionally build a custom header
```
python3 fas2rdna_cli.py --input-dir /Users/Desktop/FAS2rDNA
```

or cusomize the FASTA header
```
python3 fas2rdna_cli.py \
  --input-dir /Users/Desktop/FAS2rDNA \
  --header "{sample_id}|{seq_id}|{seq_loc}|{description}"
```

or customize the FASTA header + file name
```
python3 fas2rdna_cli.py \
  --input-dir /Users/Desktop/FAS2rDNA \
  --header "{sample_id}|{seq_id}|{seq_loc}|{description}" \
  --combined-name "All_sequences.fasta"
```

iii) Validate the results by navigating to the *fas2rdna_output* folder inside the input directory. 
#### c. Validating the results
FAS2rDNA will generate the individual .fasta file from multiple text files and the combined .fasta file, compiling all multi-FASTA sequences in one file. The result map is in the following structure:
```
/content/inputs/
├── *.txt
└── fas2rdna_output/
    ├── genomes/
    ├── fasta/
    │   ├── file1.fasta
    │   └── file2.fasta
    └── All_sequences.fasta

```

iv) Perform quality checks on the generated sequences, ensuring they are FASTA-formatted and the .fasta files are not empty.

Sample result:
```
>BLOOD_001
AAATCGGCGGACTCGGCAC ...
>LIVER_A2
TTTAAACGCCCCCACGCCT ...
>SKIN_NS
GGGCGCGTTACGTGCACGT ...
>BONE_M
TGCATTGACACCACTTCGG ...
```

---

### Supported Assemblies
The following genome assemblies are currently supported in the v.1.0 of FAS2rDNA-Colab (FAS2rDNA will detect them automatically). For more information, please refer to: [UCSC Genome Browser](https:.genome.ucsc.edu/cgi-bin/hgGateway).

- Human: hg16, hg17, hg18, hg19, hg38, hs1
- Mouse: mm7, mm8, mm9, mm10, mm39
- Rat: rn4, rn5, rn6, rn7
- Zebrafish: danRer7, danRer10, danRer11
- Fruit Fly: dm2, dm3, dm6
- *C. elegans*: ce4, ce6, ce10, ce11
- Yeast (*S. cerevisiae*): sacCer1, sacCer2, sacCer3

---

## Troubleshooting
1. No FASTA output generated
- Verify that output directory exists and that you point to a non-empty input directory
- Confirm that the *seq_loc* column exists in your data and all assemblies referenced in are supported or validated

2. FAS2rDNA is skipping entries
- Confirm that those entries contain a valid and well-formatted *seq_loc* data

3. Empty or truncated sequences
- Check coordinate validity (start < end, within chromosome bounds)
- Ensure reference FASTA files are complete and indexed

4. Incorrect strand orientation
- Confirm the strand field in *seq_loc* is correctly specified as + or -

5. Performance bottlenecks with large datasets
- Enable chunked writing or parallel execution
- Split input files by chromosome or sample batches

---

### Colab-friendly Version
Try [FAS2rDNA-Colab](https://github.com/mahvin92/FAS2rDNA-Colab)

---

### Reporting
Comments and suggestions to improve FAS2rDNA-Colab are welcome. If you find any bug or problem, please open an [issue](https://github.com/mahvin92/FAS2rDNA/issues/new).

---

### Citation
De los Santos, M. (2025). High-throughput isoform-wide miRNome sequence reconstruction in the TCGA-LUAD cohort using FAS2rDNA. Protocols.io. DOI: 10.17504/protocols.io.rm7vzenqxvx1/v1

De los Santos, M.I. (2025). FAS2rDNA-Colab: A cloud-based workflow for pan-cancer, isoform-wide miRNome reconstitution across TCGA cohorts. Protocols.io DOI: 10.17504/protocols.io.14egn1xr6v5d/v1

---

### Acknowledgement
FAS2rDNA-Colab is powered by [ChordexBio](https://chordexbio.com/) and [CodeEnigma](https://github.com/KrishnanSG/codeenigma), made with Python, and tested using Google Colab ❤️


