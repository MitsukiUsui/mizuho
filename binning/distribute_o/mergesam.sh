#!/bin/bash

#SBATCH --job-name=mergesam
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --output=./log/mergesam_%A_%a.out
#SBATCH --err=./log/mergesam_%A_%a.err
#SBATCH --mem=10g
#SBATCH --time=0-03 

FORCE_MODE=false

argFilepath=${1}
line=`awk -v line=$SLURM_ARRAY_TASK_ID '{if (NR == line) print$0}' ${argFilepath}`

module load samtools

numAssem=`echo ${line} | cut -d ',' -f1`
idx=$(( 2+$numAssem))
mergeFilepath=`echo ${line} | cut -d ',' -f${idx}`
inFilepath_lst=""

echo "START: merge ${numAssem} sams to ${mergeFilepath}"
if [ "$FORCE_MODE" = false ] && [ -e ${mergeFilepath} ]; then
    echo "PASS: merged bam already exists"
else
    for i in `seq ${numAssem}`
    do
        idx=$(( $i + 1 ))
        samFilepath=`echo ${line} | cut -d ',' -f${idx}`
        echo "  START: sort and index ${samFilepath}"
        bamFilepath=${samFilepath/.sam/.bam}
        samtools view -b ${samFilepath} | samtools sort -o ${bamFilepath}
        samtools index ${bamFilepath}
        inFilepath_lst="${inFilepath_lst} ${bamFilepath}"
    done

    echo "START: merge and index"
    samtools merge --thread 8 ${mergeFilepath} ${inFilepath_lst}
    samtools index ${mergeFilepath}
fi
