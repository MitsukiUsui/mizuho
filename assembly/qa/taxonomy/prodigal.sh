#!/bin/bash

#SBATCH --job-name=prodigal
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --input=none
#SBATCH --output=./log/prodigal_%j.out
#SBATCH --error=./log/prodigal_%j.err
#SBATCH --mem=10g
#SBATCH --time=0-01 

assemDirec=${1}
echo ${assemDirec}

for scaffname in `ls ${assemDirec}`
do
    direc=${assemDirec}/${scaffname}
    seqFilepath=${direc}/seq.fna
    gffFilepath=${direc}/genes.gff
    proFilepath=${direc}/genes.faa

    time prodigal -i ${seqFilepath} \
                  -o ${gffFilepath} -f gff \
                  -a ${proFilepath}
done
