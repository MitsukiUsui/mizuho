#!/bin/bash

#SBATCH --job-name=map
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --input=none
#SBATCH --output=./log/map_%A_%a.out
#SBATCH --err=./log/map_%A_%a.err
#SBATCH --mem=20g
#SBATCH --time=0-04 

FORCE_MODE=false

argFilepath=${1}
if [ -z ${SLURM_ARRAY_TASK_ID+x} ]; then lineNum=1; else lineNum=${SLURM_ARRAY_TASK_ID}; fi;
line=`awk -v lineNum=$lineNum '{if (NR == lineNum) print $0}' ${argFilepath}`
dbFilepath=`echo ${line} | cut -d ',' -f1`
leftFilepath=`echo ${line} | cut -d ',' -f2`
rightFilepath=`echo ${line} | cut -d ',' -f3`
samFilepath=`echo ${line} | cut -d ',' -f4`

module load samtools

FORCE_MODE=false
forceFilepath=${samFilepath}
if [ "$FORCE_MODE" = false ] && [ -e ${forceFilepath} ]; then
    echo "PASS: target file already exists"
    exit
fi

mkdir -p `dirname ${samFilepath}`
time bowtie2 --threads 8 --maxins 1000 \
             -x ${dbFilepath} \
             -1 ${leftFilepath} -2 ${rightFilepath} \
             -S ${samFilepath}
source ~/mizuho/helper/helper.sh
sam2bam ${samFilepath}
samtools idxstats ${samFilepath/.sam/.bam} > ${samFilepath/.sam/.count}
