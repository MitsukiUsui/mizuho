#!/bin/bash

#SBATCH --job-name=fastqc
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --input=none
#SBATCH --output=./log/fastqc_%j.out
#SBATCH --error=./log/fastqc_%j.err
#SBATCH --mem=10g
#SBATCH --time=1-00 

inFilepath=${1}
outDirec=${2}
#outDirec=/work/GoryaninU/mitsuki/out/fastqc/mizuho/dna/row

module load fastqc
echo ${inFilepath},${outDirec}
fastqc ${inFilepath} -o ${outDirec} -t 4 --nogroup -k 5
