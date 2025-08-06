#!/bin/bash

# ==============================================================================
# CONFIGURATION FILE for Fungal Phylogenomics Pipeline
# Defines all global variables, paths, and sample lists for use across scripts.
# ==============================================================================

# --- CONDA ENVIRONMENTS ---
# You can define your conda environments here to ensure consistency.
# Use the names you have already created or plan to create.
# Example: conda create -n trim_quality fastqc trimmomatic
CONDA_TRIM_QUALITY="trim_quality"
CONDA_ASSEMBLY="assembly"
CONDA_FUNANNOTATE="funannotate_env"
CONDA_ORTHOFINDER="orthofinder_env"
CONDA_PHYLO="phylo_env"
CONDA_FASTANI="fastani_env"

# --- THREADS ---
# Number of threads/cores to use for multi-threaded tools.
THREADS=8

# --- SAMPLE LISTS ---
# Define sample IDs for different parts of the analysis.
# Note: You have slightly different lists for some steps, so I've included a few.
ALL_SAMPLES=(2 8 20 24 25 26 34 35 37 38 54 56 58 59 60 64 73 79 80 82 89 96 116 5 10 47 62)
MASH_SAMPLES=(2 8 20 24 25 26 54 56 58 59 64 66 73 79 80 82 89 96 5 10 47 62)
FASTANI_SAMPLES=(2 8 20 24 25 26 35 37 38 54 56 58 59 60 64 73 79 80 82 89 96 116 5 10 47 62)
ORTHO_SAMPLES=(2 8 20 24 25 26 54 56 58 59 64 73 79 80 82 89 96 5 10 47 62)

# --- DIRECTORY PATHS ---
# Define all input and output directories to keep the pipeline organized.
READS_DIR="./reads"
TRIM_DIR="./results_trimmed"
ASSEMBLY_DIR="./results_assembly"
QUAST_DIR="./results_quast"
MASH_DIR="./results_mash.02"
FASTANI_DIR="./results_fastani"
FUNANNOTATE_DIR="./results_funannotate"
ORTHOLOGY_DIR="./results_orthology.02"

# Paths for the phylogenomics sub-pipeline
SCO_ALIGN_DIR="./aligned_single_copy"
SCO_EXTRACT_DIR="./sco_sequences"
GENE_TREE_DIR="./gene_trees"
SUPERMATRIX_FILE="supermatrix.fasta"
ORTHOFINDER_RESULTS_DIR="${ORTHOLOGY_DIR}/proteomes/OrthoFinder/Results_Jun22"

# --- FUNANNOTATE SETTINGS ---
# Annotation-specific parameters
AUGUSTUS_MODEL="botrytis_cinerea"
BUSCO_LINEAGE="ascomycota"
FUNANNOTATE_DB="~/.funannotate_db"