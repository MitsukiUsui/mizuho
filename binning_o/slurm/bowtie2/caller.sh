#!/bin/bash

#SBATCH --job-name=bowtie2
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --input=none
#SBATCH --output=./log/bowtie2_%j.out
#SBATCH --error=./log/bowtie2_%j.err
#SBATCH --mem=10g
#SBATCH --time=0-01

module load python/3.5.0
cd ../../
./bowtie2.sh ${1} ${2} ${3} ${4}
