#!/bin/bash

#SBATCH --job-name=assign
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --input=none
#SBATCH --output=./log/assign_%j.out
#SBATCH --error=./log/assign_%j.err
#SBATCH --mem=10g
#SBATCH --time=0-01 

./taxonomy_assignment_gene.py ${1}
./taxonomy_assignment_scaffold.py ${1}
