#!/bin/bash

#SBATCH --job-name=bowtie
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --input=none
#SBATCH --output=./log/bowtie_%j.out
#SBATCH --error=./log/bowtie_%j.err
#SBATCH --mem=20g
#SBATCH --time=1-00 

scaffoldFilepath=${1}
dbFilepath=${2}
leftFilepath=${3}
rightFilepath=${4}
outFilepath=${5}

dir=`dirname ${dbFilepath}`
mkdir -p ${dir}
dir=`dirname ${outFilepath}`
mkdir -p ${dir}

module load bowtie2
time bowtie2-build ${scaffoldFilepath} ${dbFilepath}
time bowtie2 --threads 8 -x ${dbFilepath} -1 ${leftFilepath} -2 ${rightFilepath} -S ${outFilepath}
