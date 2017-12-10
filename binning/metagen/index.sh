#!/bin/bash

#SBATCH --job-name=index
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --output=./log/index_%A_%a.out
#SBATCH --err=./log/index_%A_%a.err
#SBATCH --mem=20g
#SBATCH --time=0-03 

argFilepath=${1}
if [ -z ${SLURM_ARRAY_TASK_ID+x} ]; then lineNum=1; else lineNum=${SLURM_ARRAY_TASK_ID}; fi;
line=`awk -v lineNum=$lineNum '{if (NR == lineNum) print $0}' ${argFilepath}`
scaffFilepath=`echo ${line} | cut -d ',' -f1`
dbFilepath=`echo ${line} | cut -d ',' -f2`

echo "START: build index for "${scaffoldFilepath}" in "${dbFilepath}

FORCE_MODE=false
forceFilepath=${dbFilepath}.1.bt2
if [ "$FORCE_MODE" = false ] && [ -e ${forceFilepath} ]; then
    echo "PASS: target file already exists"
    exit
fi

mkdir -p `dirname ${dbFilepath}`
time bowtie2-build --threads 12 ${scaffFilepath} ${dbFilepath}
