#!/bin/bash

#SBATCH --job-name=filter
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --input=none
#SBATCH --output=./log/filter_%j.out
#SBATCH --error=./log/filter_%j.err
#SBATCH --mem=100g
#SBATCH --time=1-00 

correctLeft=${1}
correctRight=${2}
filterLeft=${3}
filterRight=${4}

outDirec=`dirname ${filterLeft}`
mkdir -p ${outDirec}
tmpLeft=${filterLeft}.tmp
tmpRight=${filterRight}.tmp
nameFilepath=${outDirec}/names.list

echo ${correctLeft},${correctRight},${filterLeft},${filterRight}

time seqkit grep -nrvp failed ${correctLeft} > ${tmpLeft}
time seqkit grep -nrvp failed ${correctRight} > ${tmpRight}
time grep -Fx -f <(fatt name ${tmpLeft}) <(fatt name ${tmpRight}) > ${nameFilepath}
time fatt extract --file ${nameFilepath} ${tmpLeft} > ${filterLeft}
time fatt extract --file ${nameFilepath} ${tmpRight} > ${filterRight}
