#!/bin/bash

#SBATCH --job-name=prepare
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --output=./log/prepare.out
#SBATCH --err=./log/prepare.err
#SBATCH --mem=20g
#SBATCH --time=0-03 

./prepare.py
