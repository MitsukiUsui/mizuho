#!/bin/bash

#SBATCH --job-name=merge
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --input=none
#SBATCH --output=./log/merge_%j.out
#SBATCH --error=./log/merge_%j.err
#SBATCH --mem=20g
#SBATCH --time=0-01

cd ../../
./merge.sh ${1} ${2} ${3}
