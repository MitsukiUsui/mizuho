#!/bin/bash

#SBATCH --job-name=bin
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --input=none
#SBATCH --output=./log/bin_%j.out
#SBATCH --error=./log/bin_%j.err
#SBATCH --mem=100g
#SBATCH --time=0-12 

left=${1}
right=${2}
outDirec=${3}

echo ${left},${right},${outDirec}
time ~/software/SPAdes-3.11.1-Linux/bin/spades.py \
        --meta -t 12 -m 100 \
        -1 ${left} \
        -2 ${right} \
        -o ${outDirec} \
        -k 21,33,55,77,99,127
