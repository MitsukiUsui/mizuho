#!/bin/bash

#SBATCH --job-name=distfastq
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --output=./log/distfastq_%A_%a.out
#SBATCH --err=./log/distfastq_%A_%a.err
#SBATCH --mem=100g
#SBATCH --time=0-03 

FORCE_MODE=true

argFilepath=${1}
line=`awk -v line=$SLURM_ARRAY_TASK_ID '{if (NR == line) print$0}' ${argFilepath}`
sampleId=`echo ${line} | cut -d ',' -f1`

#--------------------------------------------------------------------------------
# distribute fastq
#--------------------------------------------------------------------------------
outFilepath1=/work/GoryaninU/mitsuki/out/binning/distribute/bin001/${sampleId}_R1.fastq
if [ "$FORCE_MODE" = false ] && [ -e ${outFilepath1} ]; then
    echo "PASS: fastq already distributed"
else
    ./distributefastq.py ${sampleId}
fi
