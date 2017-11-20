#!/bin/bash

#SBATCH --job-name=distribute
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --input=none
#SBATCH --output=../../log/distribute_%j.out
#SBATCH --error=../../log/distribute_%j.err
#SBATCH --mem=50g
#SBATCH --time=0-01

module load python/3.5.0
sampleId=${1}
echo ${sampleId}
../../distribute.py ${sampleId}
