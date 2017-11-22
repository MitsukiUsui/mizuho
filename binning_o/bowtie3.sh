#!/bin/bash

#SBATCH --job-name=bowtie3
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --input=none
#SBATCH --output=./log/bowtie3_%j.out
#SBATCH --error=./log/bowtie3_%j.err
#SBATCH --mem=20g
#SBATCH --time=0-04 

binId=${1}
binDirec=/work/GoryaninU/mitsuki/out/binning/bin/bin`printf "%03d" ${binId}`
module load samtools

echo ${binDirec}
array=(18m anode chamber random)
for type in ${array[@]}
do
    samFilepath=${binDirec}/${type}.sam
    bamFilepath=${binDirec}/${type}.bam
    echo ${samFilepath}
    samtools view -Sb ${samFilepath} | samtools sort -o ${bamFilepath}
    samtools index ${bamFilepath}
done

outFilepath=${binDirec}/original.bam
samtools merge --thread 8 \
   ${outFilepath} \
   ${binDirec}/18m.bam \
   ${binDirec}/anode.bam \
   ${binDirec}/chamber.bam \
   ${binDirec}/random.bam
samtools index ${outFilepath}
