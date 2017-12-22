#!/bin/bash

#SBATCH --job-name=divide
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --input=none
#SBATCH --output=./log/divide_%A_%a.out
#SBATCH --error=./log/divide_%A_%a.err
#SBATCH --mem=30g
#SBATCH --time=0-04

argFilepath=${1}
if [ -z ${SLURM_ARRAY_TASK_ID+x} ]; then lineNum=1; else lineNum=${SLURM_ARRAY_TASK_ID}; fi;
line=`awk -v lineNum=$lineNum '{if (NR == lineNum) print $0}' ${argFilepath}`
sampleId=`echo ${line} | cut -d ',' -f1`

echo "START: process ${sampleId}"
FORCE_MODE=false
forceFilepath=/work/GoryaninU/mitsuki/out/distribute/ref/ref067/${sampleId}_R2.fastq
if [ "$FORCE_MODE" = false ] && [ -e ${forceFilepath} ]; then
    echo "PASS: target file already exists"
    exit
fi

./create_ref.py ${sampleId}
./distribute_fastq.py ${sampleId}
