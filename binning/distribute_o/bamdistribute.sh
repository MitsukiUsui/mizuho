#!/bin/bash

#SBATCH --job-name=distbam
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --output=./log/distbam_%A_%a.out
#SBATCH --err=./log/distbam_%A_%a.err
#SBATCH --mem=60g
#SBATCH --time=0-03 

FORCE_MODE=false

argFilepath=${1}
line=`awk -v line=$SLURM_ARRAY_TASK_ID '{if (NR == line) print$0}' ${argFilepath}`

assemName=`echo ${line} | cut -d ',' -f1`
inFilepath_lst=`echo ${line} | cut -d ',' -f2`
mergeFilepath=`echo ${line} | cut -d ',' -f3` #assume bam
numBins=`echo ${line} | cut -d ',' -f4`

module load samtools

#--------------------------------------------------------------------------------
# merge bams into one
#--------------------------------------------------------------------------------
echo "START: merge bams to "${mergeFilepath}
if [ "$FORCE_MODE" = false ] && [ -e ${mergeFilepath} ]; then
    echo "PASS: merged bam already exists"
else
    dir=`dirname ${mergeFilepath}`
    mkdir -p ${dir}
    time samtools merge --threads 8 -f ${mergeFilepath} ${inFilepath_lst}
    samtools view -h -o ${mergeFilepath/.bam/.sam} ${mergeFilepath}
    echo "DONE: merge bams"
fi

#--------------------------------------------------------------------------------
# output header to each sams
#--------------------------------------------------------------------------------
echo "START: output header to "${numBins}" sams"
for binId in `seq -f %03g ${numBins}`
do
    binFilepath=/work/GoryaninU/mitsuki/out/binning/distribute/bin${binId}/${assemName}.sam
    samtools view -H -o ${mergeFilepath} ${binFilepath}
    echo "  DONE: "${binFilepath}
done

#--------------------------------------------------------------------------------
# distribute sams
#--------------------------------------------------------------------------------
./bamdistribute.py ${assemName}
