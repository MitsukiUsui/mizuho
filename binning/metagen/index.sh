#!/bin/bash

#SBATCH --job-name=index
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --output=./log/index_%A_%a.out
#SBATCH --err=./log/index_%A_%a.err
#SBATCH --mem=20g
#SBATCH --time=0-03 

FORCE_MODE=false

argFilepath=${1}
line=`awk -v line=$SLURM_ARRAY_TASK_ID '{if (NR == line) print$0}' ${argFilepath}`
scaffFilepath=`echo ${line} | cut -d ',' -f1`
dbFilepath=`echo ${line} | cut -d ',' -f2`

echo ${scaffFilepath},${dbFilepath}
echo "START: build index for "${scaffoldFilepath}" in "${dbFilepath}
if [ "$FORCE_MODE" = false ] && [ -e ${dbFilepath}.1.bt2 ]; then
    echo "PASS: index already exists"
else
    dir=`dirname ${dbFilepath}`
    mkdir -p ${dir}
    time bowtie2-build --threads 12 ${scaffFilepath} ${dbFilepath}
    echo "DONE: build index"
fi
