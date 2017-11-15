#!/bin/bash

#SBATCH --job-name=samfilter
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --input=none
#SBATCH --output=./log/samfilter_%j.out
#SBATCH --error=./log/samfilter_%j.err
#SBATCH --mem=10g
#SBATCH --time=1-00 

fp1_s="demo.sam" #input
fp2_b="demo.bam" #indexed bam
fp3_s="filter.sam" #filtered sam
fp4_b="filter.bam" #filtered, sorted bam
fp5="filter.depth"

module load samtools

#sort and add index
samtools view -Sb ${fp1_s} | samtools sort -o ${fp2_b}
samtools index ${fp2_b}

#filter by seq name
samtools view -H ${fp2_b} > ${fp3_s}
while read line
do
    samtools view ${fp2_b} ${line} >> ${fp3_s}
done < seq.list
samtools view -Sb ${fp3_s} | samtools sort -o ${fp4_b}

samtools depth ${fp4_b} -o ${fp5}

