#!/bin/bash

#SBATCH --job-name=all
#SBATCH --partition=largemem
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=22
#SBATCH --input=none
#SBATCH --output=./log/all.out
#SBATCH --error=./log/all.err
#SBATCH --mem=500g
#SBATCH --time=7-00 

out=/work/GoryaninU/mitsuki/out/spades/36m_trim/all

time ~/software/SPAdes-3.11.1-Linux/bin/spades.py \
        --meta -t 22 -m 500 \
        --dataset all.yaml \
        -o ${out} \
        -k 21,33,55,77,99,127

