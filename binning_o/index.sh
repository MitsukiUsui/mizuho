#!/bin/bash

#SBATCH --job-name=index
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --input=none
#SBATCH --output=./log/index_%j.out
#SBATCH --error=./log/index_%j.err
#SBATCH --mem=20g
#SBATCH --time=0-03 

scaffoldFilepath=${1}
dbFilepath=${2}
echo ${scaffoldFilepath},${dbFilepath}

dir=`dirname ${dbFilepath}`
mkdir -p ${dir}

time bowtie2-build --threads 12 ${scaffoldFilepath} ${dbFilepath}
