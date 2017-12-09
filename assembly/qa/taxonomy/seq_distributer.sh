#!/bin/bash

#SBATCH --job-name=seqdist
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --input=none
#SBATCH --output=./log/seqdist_%j.out
#SBATCH --error=./log/seqdist_%j.err
#SBATCH --mem=10g
#SBATCH --time=0-01 

./seq_distributer.py ${1} ${2}
