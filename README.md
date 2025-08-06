# Fungal Phylogenomics Pipeline

This document serves as supplementary material for the final report and provides a detailed description of the computational methods used.

## Pipeline Overview

The analysis is broken down into a series of numbered bash scripts (`bin/`), which orchestrate the entire workflow. Each script performs a specific, well-defined task, allowing for easy troubleshooting and modular execution.

The pipeline covers the following major steps:

1.  **Read Quality Control & Trimming**: Initial processing of raw sequencing reads.
2.  **De Novo Assembly**: Construction of genome assemblies from trimmed reads.
3.  **Assembly Quality Assessment**: Evaluation of assembly quality using multiple metrics.
4.  **Genome Annotation**: Identification and functional annotation of genes.
5.  **Comparative Genomics**: Whole-genome comparisons to determine relatedness.
6.  **Phylogenomics**: Inference of species-level evolutionary relationships using multiple methods.

---

### Step 1: Pre-processing and Assembly

The initial scripts handle the raw data and build the foundational genome assemblies.

| File Name | Description |
| :--- | :--- |
| `01_trimming_and_fastqc.sh` | Runs **FastQC** for quality reports and **Trimmomatic** for adapter removal and quality trimming on raw paired-end reads. |
| `02_assembly_spades.sh` | Performs *de novo* genome assembly using **SPAdes** on the trimmed reads. |
| `03_quast_evaluation.sh` | Evaluates the quality of each SPAdes assembly using **QUAST**. |
| `04_summarize_quast_results.sh` | Parses the individual QUAST reports and consolidates key metrics (`# contigs`, `Total length`, `N50`, `GC %`) into a single summary file. |
| `scripts/plot_quast_metrics.py` | Generates bar plots from the QUAST summary to visualize assembly quality across samples. |

---

### Step 2: Comparative Genomics

These scripts use whole-genome approaches to measure relatedness between the fungal isolates.

| File Name | Description |
| :--- | :--- |
| `05_mash_analysis.sh` | Uses **Mash** to compute genome-wide distances and create a preliminary distance-based tree in Newick format. |
| `scripts/plot_mash_dendrogram.py` | Plots a hierarchical dendrogram from the Mash distance data, with sample labels and group assignments. |
| `scripts/plot_mash_heatmap.py` | Visualizes the Mash distances as a clustered heatmap for a different perspective on genomic similarity. |
| `06_fastani_analysis.sh` | Calculates **Average Nucleotide Identity (ANI)** between all assembled genomes using **FastANI**. |
| `scripts/plot_fastani_dendrogram.py` | Creates a dendrogram from the FastANI distance matrix (`100 - ANI`), providing another view of species relatedness. |

---

### Step 3: Gene Prediction and Orthology

This section focuses on identifying and annotating genes, and then grouping them into orthologous families.

| File Name | Description |
| :--- | :--- |
| `07_funannotate_prediction.sh` | Runs the **Funannotate** pipeline for gene prediction and annotation, including contig filtering and repeat masking. It generates protein and nucleotide FASTA files for each sample. |
| `08_prepare_proteomes_for_orthofinder.sh` | Copies the protein FASTA files from the Funannotate results to a dedicated directory for OrthoFinder. |
| `09_run_orthofinder.sh` | Executes **OrthoFinder** to identify orthologous gene groups and infer a species tree from all gene trees. |
| `scripts/plot_orthogroup_upset.py` | Generates an **UpSet plot** to visualize the number and overlap of orthogroups across the different species. |

---

### Step 4: Phylogenomics

These scripts perform phylogenetic analysis using a variety of methods based on single-copy orthologs.

| File Name | Description |
| :--- | :--- |
| `10_run_phylogenomics_pipeline.sh` | A master script that orchestrates the following: <br> • **Single-Copy Ortholog (SCO) Extraction**: Identifies and extracts SCOs from OrthoFinder results. <br> • **Sequence Alignment**: Aligns each SCO protein family using **MAFFT**. <br> • **Gene Tree Inference**: Builds a phylogenetic tree for each aligned SCO using **IQ-TREE**. <br> • **Supermatrix Concatenation**: Combines all aligned SCOs into a single supermatrix. <br> • **Species Tree Inference**: Infers a final species tree from the supermatrix (concatenation approach) and a consensus tree from all individual gene trees. |
| `scripts/extract_scos.py` | A Python script called by `10_run_phylogenomics_pipeline.sh` to parse the `Orthogroups.GeneCount.tsv` file and identify SCOs. |
| `scripts/extract_sco_seqs.py` | A Python script to extract the actual protein sequences for each SCO from the Funannotate protein FASTA files. |
| `scripts/build_supermatrix.py` | A Python script to concatenate all aligned SCOs into one large FASTA file for phylogenetic inference. |

---

## Required Software

This pipeline relies on several bioinformatics tools, all of which are managed via **Conda**. The scripts are written to activate specific Conda environments as needed.

* FastQC
* Trimmomatic
* SPAdes
* QUAST
* Mash
* FastANI
* Funannotate
* OrthoFinder
* MAFFT
* IQ-TREE
* Biopython
* pandas
* matplotlib
* seaborn
* scipy

## How to Re-run the Analysis

1.  **Clone this repository** to your local machine.
2.  **Install Conda** and the necessary environments. The `bin/` directory contains several `*_env_setup.sh` scripts that can create these environments for you, or you can create them manually from the provided `environments/*.yml` files.
3.  **Place your raw reads** in the `data/reads/` directory. The scripts expect files to be named `[sample_id]_1.fq.gz` and `[sample_id]_2.fq.gz`.
4.  **Edit `bin/00_config.sh`** to match your file paths, sample IDs, and other parameters.
5.  **Run the scripts in numerical order** from the `bin/` directory.

```bash
# Example
cd your_project_name/
bash bin/01_trimming_and_fastqc.sh
bash bin/02_assembly_spades.sh
...