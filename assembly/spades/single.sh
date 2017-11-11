#!/bin/bash

#SBATCH --job-name=single
#SBATCH --partition=largemem
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --input=none
#SBATCH --output=./log/single_%j.out
#SBATCH --error=./log/single_%j.err
#SBATCH --mem=100g
#SBATCH --time=0-12 

left=${1}
right=${2}
outDirec=${3}

echo ${left},${right},${outDirec}
time ~/software/SPAdes-3.11.1-Linux/bin/spades.py \
        --meta -t 10 -m 100 \
        -1 ${left} \
        -2 ${right} \
        -o ${outDirec} \
        -k 21,33,55,77,99,127
