#!/bin/bash

#SBATCH --job-name=prodigal
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --input=none
#SBATCH --output=./log/prodigal_%A_%a.out
#SBATCH --error=./log/prodigal_%A_%a.err
#SBATCH --mem=10g
#SBATCH --time=0-01 

argFilepath=${1}
if [ -z ${SLURM_ARRAY_TASK_ID+x} ]; then lineNum=1; else lineNum=${SLURM_ARRAY_TASK_ID}; fi;
line=`awk -v lineNum=$lineNum '{if (NR == lineNum) print $0}' ${argFilepath}`
echo ${argFilepath}
cat ${argFilepath}
echo ${SLURM_ARRAY_TASK_ID}
echo ${lineNum}
echo ${line}
assemDirec=`echo ${line} | cut -d ',' -f1`
echo ${assemDirec}

for scaffName in `ls ${assemDirec}`
do
    direc=${assemDirec}/${scaffName}
    seqFilepath=${direc}/seq.fna
    gffFilepath=${direc}/genes.gff
    proFilepath=${direc}/genes.faa

    time prodigal -i ${seqFilepath} \
                  -o ${gffFilepath} -f gff \
                  -a ${proFilepath}
done
