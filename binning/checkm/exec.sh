#!/bin/bash

#SBATCH --job-name=checkm
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
#SBATCH --input=none
#SBATCH --output=./log/checkm_%A_%a.out
#SBATCH --error=./log/checkm_%A_%a.err
#SBATCH --mem=120g
#SBATCH --time=0-04

baseDirec=/work/GoryaninU/mitsuki/out/checkm/36m_anode/refine
#checkm lineage_wf --threads 24 -x fasta ${baseDirec}/in ${baseDirec}/out
checkm lineage_wf --threads 24 ${baseDirec}/in ${baseDirec}/out
