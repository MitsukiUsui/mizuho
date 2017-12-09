#!/bin/bash

#SBATCH --job-name=genemerge
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --input=none
#SBATCH --output=./log/genemerge_%j.out
#SBATCH --error=./log/genemerge_%j.err
#SBATCH --mem=10g
#SBATCH --time=0-01 

./gene_merger.py ${1} ${2}
