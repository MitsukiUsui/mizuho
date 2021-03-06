#!/bin/bash

#SBATCH --job-name=diamond
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --input=none
#SBATCH --output=./log/diamond_%A_%a.out
#SBATCH --error=./log/diamond_%A_%a.err
#SBATCH --mem=20g
#SBATCH --time=0-01

argFilepath=${1}
if [ -z ${SLURM_ARRAY_TASK_ID+x} ]; then lineNum=1; else lineNum=${SLURM_ARRAY_TASK_ID}; fi;
line=`awk -v lineNum=$lineNum '{if (NR == lineNum) print $0}' ${argFilepath}`
dbFilepath=`echo ${line} | cut -d ',' -f1`
queryFilepath=`echo ${line} | cut -d ',' -f2`
outFilepath=`echo ${line} | cut -d ',' -f3`

FORCE_MODE=true
forceFilepath=${outFilepath}
if [ "$FORCE_MODE" = false ] && [ -e ${forceFilepath} ]; then
    echo "PASS: target file already exists"
    exit
fi

diamond blastp --threads 8 \
               -d ${dbFilepath} \
               -q ${queryFilepath} \
               -o ${outFilepath}
