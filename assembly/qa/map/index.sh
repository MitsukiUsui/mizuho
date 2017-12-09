#!/bin/bash

#SBATCH --job-name=index
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --input=none
#SBATCH --output=./log/index_%A_%j.out
#SBATCH --error=./log/index_%A_%j.err
#SBATCH --mem=20g
#SBATCH --time=1-00 

argFilepath=${1}
if [ -z ${SLURM_ARRAY_TASK_ID+x} ]; then lineNum=1; else lineNum=${SLURM_ARRAY_TASK_ID}; fi;
line=`awk -v lineNum=$lineNum '{if (NR == lineNum) print $0}' ${argFilepath}`
mapper=`echo ${line} | cut -d ',' -f1`
seqFilepath=`echo ${line} | cut -d ',' -f2`
dbFilepath=`echo ${line} | cut -d ',' -f3`

echo "START: build index for ${mapper}"
if [ "$mapper" = bowtie ]; then
    time bowtie2-build --thread 8 ${seqFilepath} ${dbFilepath}
elif [ "$mapper" = bwa ]; then
    module load bwa.gcc/0.7.10
    time bwa index -p ${dbFilepath} ${seqFilepath}
fi
