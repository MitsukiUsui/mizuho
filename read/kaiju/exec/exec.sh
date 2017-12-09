#!/bin/bash

#SBATCH --job-name=kaiju
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --input=none
#SBATCH --output=./log/kaiju_%A_%a.out
#SBATCH --error=./log/kaiju_%A_%a.err
#SBATCH --mem=100g
#SBATCH --time=1-00 


#--------------------------------------------------------------------------------
# array job expander
#--------------------------------------------------------------------------------
argFilepath=${1}
if [ -z ${SLURM_ARRAY_TASK_ID+x} ]; then lineNum=1; else lineNum=${SLURM_ARRAY_TASK_ID}; fi;
line=`awk -v lineNum=$lineNum '{if (NR == lineNum) print $0}' ${argFilepath}`
nodesFilepath=`echo ${line} | cut -d ',' -f1`
namesFilepath=`dirname ${nodesFilepath}`/names.dmp
dbFilepath=`echo ${line} | cut -d ',' -f2`
forwardFilepath=`echo ${line} | cut -d ',' -f3`
reverseFilepath=`echo ${line} | cut -d ',' -f4`
outFilepath=`echo ${line} | cut -d ',' -f5`
genusFilepath=${outFilepath/.tsv/.genus}

echo "START: output ${outFilepath}"

FORCE_MODE=false
forceFilepath=${outFilepath}
if [ "$FORCE_MODE" = false ] && [ -e ${forceFilepath} ]; then
    echo "PASS: target file already exists"
else
    time kaiju -t ${nodesFilepath} -f ${dbFilepath} \
               -i ${forwardFilepath} -j ${reverseFilepath} \
               -o ${outFilepath} \
               -z 8
    echo "DONE: output ${outFilepath}"
fi

kaijuReport -t ${nodesFilepath} -n ${namesFilepath} \
            -i ${outFilepath} \
            -r genus \
            -o ${genusFilepath}
echo "DONE: output ${genusFilepath}"
