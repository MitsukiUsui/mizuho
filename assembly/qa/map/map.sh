#!/bin/bash

#SBATCH --job-name=map
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --input=none
#SBATCH --output=./log/map_%A_%a.out
#SBATCH --error=./log/map_%A_%a.err
#SBATCH --mem=20g
#SBATCH --time=1-00 

argFilepath=${1}
if [ -z ${SLURM_ARRAY_TASK_ID+x} ]; then lineNum=1; else lineNum=${SLURM_ARRAY_TASK_ID}; fi;
line=`awk -v lineNum=$lineNum '{if (NR == lineNum) print $0}' ${argFilepath}`
mapper=`echo ${line} | cut -d ',' -f1`
dbFilepath=`echo ${line} | cut -d ',' -f2`
leftFilepath=`echo ${line} | cut -d ',' -f3`
rightFilepath=`echo ${line} | cut -d ',' -f4`
samFilepath=`echo ${line} | cut -d ',' -f5`

mkdir -p `dirname ${samFilepath}`
echo "START: map with ${mapper}"

if [ "$mapper" = bowtie ]; then
    time bowtie2 -a --threads 8 --maxins 1000 \
                 -x ${dbFilepath} \
                 -1 ${leftFilepath} -2 ${rightFilepath} \
                 -S ${samFilepath}
elif [ "$mapper" = bwa ]; then
    module load bwa.gcc/0.7.10
    time bwa mem -a -t 8 ${dbFilepath} ${leftFilepath} ${rightFilepath} > ${samFilepath}
fi

source ~/mizuho/helper/helper.sh
sam2bam ${samFilepath}
