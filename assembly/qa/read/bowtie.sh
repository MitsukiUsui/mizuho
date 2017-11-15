#!/bin/bash

#SBATCH --job-name=bowtie
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --input=none
#SBATCH --output=./log/bowtie_%j.out
#SBATCH --error=./log/bowtie_%j.err
#SBATCH --mem=20g
#SBATCH --time=1-00 

scaffoldFilepath=${1}
dbFilepath=${2}
leftFilepath=${3}
rightFilepath=${4}
samFilepath=${5}
insertFilepath=${6}

echo ${scaffoldFilepath},${dbFilepath},${leftFilepath},${rightFilepath},${samFilepath},${insertFilepath}

array=(${dbFilepath} ${samFilepath} ${insertFilepath})
for filepath in ${array[@]}
do
    dir=`dirname ${filepath}`
    mkdir -p ${dir}
done

#module load bowtie2
#time bowtie2-build ${scaffoldFilepath} ${dbFilepath}
#time bowtie2 --threads 8 --maxins 1000 \
#             -x ${dbFilepath} \
#             -1 ${leftFilepath} -2 ${rightFilepath} \
#             -S ${samFilepath}
cut -f 9 ${samFilepath} |sed '/^\s*$/d' | sort -n | uniq -c | sed -e 's/ *//' -e 's/ /,/' > ${insertFilepath}
