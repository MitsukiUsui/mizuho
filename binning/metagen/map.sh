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
line=`awk -v line=$SLURM_ARRAY_TASK_ID '{if (NR == line) print$0}' ${argFilepath}`

dbFilepath=`echo ${line} | cut -d ',' -f1`
leftFilepath=`echo ${line} | cut -d ',' -f2`
rightFilepath=`echo ${line} | cut -d ',' -f3`
samFilepath=`echo ${line} | cut -d ',' -f4`
sortFilepath=${samFilepath/.sam/.bam}
countFilepath=${samFilepath/.sam/.count}

dir=`dirname ${samFilepath}`
mkdir -p ${dir}
module load samtools

echo "START: map ${leftFilepath} to ${dbFilepath}"
if  [ "$FORCE_MODE" = false ] && [ -e ${samFilepath} ]; then
    echo "PASS: sam already exists"
else
    time bowtie2 --threads 8 --maxins 1000 -a \
                 -x ${dbFilepath} \
                 -1 ${leftFilepath} -2 ${rightFilepath} \
                 -S ${samFilepath}
    samtools view -Sb ${samFilepath} | samtools sort -o ${sortFilepath}
    samtools index ${sortFilepath}
    samtools idxstats ${sortFilepath} > ${countFilepath}
fi
