#!/bin/bash

#SBATCH --job-name=checkm
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --input=none
#SBATCH --output=./log/checkm_%A_%a.out
#SBATCH --error=./log/checkm_%A_%a.err
#SBATCH --mem=100g
#SBATCH --time=0-04

checkm lineage_wf --threads 8 -x fasta /work/GoryaninU/mitsuki/out/checkm/mycc/in /work/GoryaninU/mitsuki/out/checkm/mycc/out
