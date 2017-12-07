#!/bin/bash

#SBATCH --job-name=pool
#SBATCH --partition=largemem
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --input=none
#SBATCH --output=./log/pool_%j.out
#SBATCH --error=./log/pool_%j.err
#SBATCH --mem=250g
#SBATCH --time=2-00 

yaml=${1}
outDirec=${2}

echo ${yaml},${outDirec}
time ~/software/SPAdes-3.11.1-Linux/bin/spades.py \
        --meta --only-assembler \
        -t 12 -m 250 \
        --dataset ${yaml} \
        -o ${outDirec} \
        -k 21,33,55,77,99,127

