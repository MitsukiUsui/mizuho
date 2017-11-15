#!/bin/bash

#SBATCH --job-name=stats
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --input=none
#SBATCH --output=./log/stats_%j.out
#SBATCH --error=./log/stats_%j.err
#SBATCH --mem=20g
#SBATCH --time=1-00 

seqFilepath=${1}
statsFilepath=${2}
echo ${seqFilepath},${statsFilepath}
time seqkit stats -T ${seqFilepath} > ${statsFilepath}
