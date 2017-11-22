#!/bin/bash

#SBATCH --job-name=mergebam
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --input=none
#SBATCH --output=./log/mergebam_%j.out
#SBATCH --error=./log/mergebam_%j.err
#SBATCH --mem=20g
#SBATCH --time=0-01

cd ../../
./mergebam.sh $@
