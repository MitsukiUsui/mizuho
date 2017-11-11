#!/bin/bash

#SBATCH --job-name=trim
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --input=none
#SBATCH --output=./log/trim_%j.out
#SBATCH --error=./log/trim_%j.err
#SBATCH --mem=20g
#SBATCH --time=1-00 

inLeftFilepath=${1}
inRightFilepath=${2}
outLeftFilepath=${3}
outRightFilepath=${4}
tmpLeftFilepath=${outLeftFilepath/.fastq/.tmp.fastq}
tmpRightFilepath=${outRightFilepath/.fastq/.tmp.fastq}

time cutadapt -a AGATCGGAAGAGCACACGTCTGAACTCCAGTCA \
              -A AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT \
              -o ${tmpLeftFilepath} \
              -p ${tmpRightFilepath} \
              --minimum-length 100 \
              ${inLeftFilepath} ${inRightFilepath}

time cutadapt --cut 10 --cut -5 \
              -o ${outLeftFilepath} ${tmpLeftFilepath}
time cutadapt --cut 10 --cut -5 \
              -o ${outRightFilepath} ${tmpRightFilepath}
rm ${tmpLeftFilepath}
rm ${tmpRightFilepath}
