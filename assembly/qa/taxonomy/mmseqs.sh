#!/bin/bash

#SBATCH --job-name=mmseqs
#SBATCH --partition=largemem
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --input=none
#SBATCH --output=./log/mmseqs_%j.out
#SBATCH --error=./log/mmseqs_%j.err
#SBATCH --mem=250g
#SBATCH --time=0-05 

baseDirec=${1}
mmseqsDirec=${baseDirec}/mmseqs
seqFilepath=${mmseqsDirec}/merge.faa
queryDb=${mmseqsDirec}/query
resultDb=${mmseqsDirec}/result
resultTsv=${mmseqsDirec}/result.m8
bestTsv=${mmseqsDirec}/result.best
tmpDirec=${mmseqsDirec}/tmp
targetDb="/work/GoryaninU/mitsuki/blast/nr2/targetDB"

FORCE_MODE=false
forceFilepath=${bestTsv}
if [ "$FORCE_MODE" = false ] && [ -e ${forceFilepath} ]; then
    echo "PASS: target file already exists"
else
    echo "START: ${mmseqsDirec}"

    mkdir -p ${tmpDirec}
    time -p {
        mmseqs createdb ${seqFilepath} ${queryDb}
        mmseqs search -s 1 --threads 12 ${queryDb} ${targetDb} ${resultDb} ${tmpDirec}
        mmseqs convertalis --threads 12 ${queryDb} ${targetDb} ${resultDb} ${resultTsv}
        sort -k1,1 -k12,12nr -k11,11n  ${resultTsv} | sort -u -k1,1 --merge > ${bestTsv}
    }
fi
