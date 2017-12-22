#!/bin/bash

#SBATCH --job-name=mergefastq
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --output=./log/mergefastq_%A_%a.out
#SBATCH --err=./log/mergefastq_%A_%a.err
#SBATCH --mem=30g
#SBATCH --time=0-03 

FORCE_MODE=true

binId=`printf "%03d" $SLURM_ARRAY_TASK_ID`
binDirec=/work/GoryaninU/mitsuki/out/binning/distribute/bin${binId}
outLeftFilepath=${binDirec}/bin${binId}_R1.fastq
outRightFilepath=${binDirec}/bin${binId}_R2.fastq
sampleListFilepath="../list/sample.list"

echo ${binDirec},${outLeftFilepath},${outRightFilepath}
if [ "$FORCE_MODE" = false ] && [ -e ${outLeftFilepath} ]; then
    echo "PASS: merged fastq already exists"
else
    rm ${outLeftFilepath}
    rm ${outRightFilepath}
    sed 1d ${sampleListFilepath} | while read line
    do
        left=`echo ${line}|cut -d "," -f2`
        right=`echo ${line}|cut -d "," -f3`
        inLeftFilepath=${binDirec}/`basename ${left}`
        inRightFilepath=${binDirec}/`basename ${right}`
        cat ${inLeftFilepath} >> ${outLeftFilepath}
        cat ${inRightFilepath} >> ${outRightFilepath}
    done
fi
