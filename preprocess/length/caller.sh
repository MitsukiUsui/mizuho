#!/bin/bash

#SBATCH --job-name=length
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --input=none
#SBATCH --output=./log/length_%j.out
#SBATCH --error=./log/length_%j.err
#SBATCH --mem=10g
#SBATCH --time=1-00 


inFilepath=${1}
outFilepath=${2}
thres=${3}
echo ${inFilepath},${outFilepath},${thres}
seqkit seq -m ${thres} ${inFilepath} > ${outFilepath}
