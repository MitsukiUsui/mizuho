#!/bin/bash

#SBATCH --job-name=bowtie
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --input=none
#SBATCH --output=./log/bowtie_%j.out
#SBATCH --error=./log/bowtie_%j.err
#SBATCH --mem=20g
#SBATCH --time=0-04 

dbFilepath=${1}
leftFilepath=${2}
rightFilepath=${3}
samFilepath=${4}
sortFilepath=${samFilepath/.sam/.bam}
countFilepath=${samFilepath/.sam/.count}

echo ${dbFilepath},${samFilepath}

dir=`dirname ${samFilepath}`
mkdir -p ${dir}

module load samtools
time bowtie2 --threads 8 --maxins 1000 \
             -x ${dbFilepath} \
             -1 ${leftFilepath} -2 ${rightFilepath} \
             -S ${samFilepath}
samtools view -Sb ${samFilepath} | samtools sort -o ${sortFilepath}
samtools index ${sortFilepath}
samtools idxstats ${sortFilepath} > ${countFilepath}
