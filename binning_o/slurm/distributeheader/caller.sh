#!/bin/bash

#SBATCH --job-name=header
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --input=none
#SBATCH --output=./log/header_%j.out
#SBATCH --error=./log/header_%j.err
#SBATCH --mem=20g
#SBATCH --time=0-01

cd ../../
./distributeheader.sh ${1} ${2}
