#!/bin/bash

#SBATCH --job-name=bowtie
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-par-task=8
#SBATCH --input=none
#SBATCH --output=./log/bowtie_%j.out
#SBATCH --error=./log/bowtie_%j.err
#SBATCH --mem=20g
#SBATCH --time=0-04 

scaffoldFilepath=${1}
leftFilepath=${2}
rightFilepath=${3}
samFilepath=${4}
dbFilepath=${scaffoldFilepath/.fasta/}
sortFilepath=${samFilepath/.sam/.bam}

echo ${scaffoldFilepath},${dbFilepath},${leftFilepath},${rightFilepath},${samFilepath}

module load samtools
time bowtie2-build --threads 8 ${scaffoldFilepath} ${dbFilepath}
time bowtie2 --threads 8 --maxins 1000 -a\
             -x ${dbFilepath} \
             -1 ${leftFilepath} -2 ${rightFilepath} \
             -S ${samFilepath}
samtools view -Sb ${samFilepath} | samtools sort -o ${sortFilepath}
samtools index ${sortFilepath}
