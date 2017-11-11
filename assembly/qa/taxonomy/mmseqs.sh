#!/bin/bash

#SBATCH --job-name=mmseqs
#SBATCH --partition=largemem
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
#SBATCH --input=none
#SBATCH --output=./log/mmseqs_%j.out
#SBATCH --error=./log/mmseqs_%j.err
#SBATCH --mem=250g
#SBATCH --time=0-05 

baseDirec=/work/GoryaninU/mitsuki/out/taxonomy
mmseqsDirec=${baseDirec}/mmseqs

seqFilepath=${mmseqsDirec}/merge.fna
queryDb=${mmseqsDirec}/query
resultDb=${mmseqsDirec}/result
resultTsv=${mmseqsDirec}/result.m8
tmpDirec=${mmseqsDirec}/tmp

targetDb="/work/GoryaninU/mitsuki/blast/nr2/targetDB"

mkdir -p ${tmpDirec}
mmseqs createdb ${seqFilepath} ${queryDb}
mmseqs search -s 1 ${queryDb} ${targetDb} ${resultDb} ${tmpDirec}
mmseqs convertalis ${queryDb} ${targetDb} ${resultDb} ${resultTsv}
