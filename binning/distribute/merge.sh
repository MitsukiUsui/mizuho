#!/bin/bash

#SBATCH --job-name=merge
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --input=none
#SBATCH --output=./log/merge_%A_%a.out
#SBATCH --error=./log/merge_%A_%a.err
#SBATCH --mem=20g
#SBATCH --time=0-04

argFilepath=${1}
prevArgFilepath=${2}

if [ -z ${SLURM_ARRAY_TASK_ID+x} ]; then lineNum=1; else lineNum=${SLURM_ARRAY_TASK_ID}; fi;
line=`awk -v lineNum=$lineNum '{if (NR == lineNum) print $0}' ${argFilepath}`
binId=`echo ${line} | cut -d ',' -f1`

sampleId_arr=`cat ${prevArgFilepath}`
binDirec=/work/GoryaninU/mitsuki/out/distribute/ref/ref${binId}

echo "START: merge files under ${binDirec}"
direction_arr=("R1" "R2")
for direction in ${direction_arr[@]}
do
    outFilepath=${binDirec}/ref${binId}_${direction}.fastq
    rm ${outFilepath}
    for sampleId in ${sampleId_arr[@]}
    do
        inFilepath=${binDirec}/${sampleId}_${direction}.fastq
        echo ${inFilepath}
        cat ${inFilepath} >> ${outFilepath}
    done
done
