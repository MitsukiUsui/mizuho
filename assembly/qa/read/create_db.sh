#!/bin/bash

#SBATCH --job-name=db
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --input=none
#SBATCH --output=./log/db_%A_%a.out
#SBATCH --error=./log/db_%A_%a.err
#SBATCH --mem=20g
#SBATCH --time=1-00 

argFilepath=${1}
if [ -z ${SLURM_ARRAY_TASK_ID+x} ]; then lineNum=1; else lineNum=${SLURM_ARRAY_TASK_ID}; fi;
line=`awk -v lineNum=$lineNum '{if (NR == lineNum) print $0}' ${argFilepath}`
dbFilepath=`echo ${line} | cut -d ',' -f1`
fastqFilepath=`echo ${line} | cut -d ',' -f2`
scaffFilepath=`echo ${line} | cut -d ',' -f3`
bowtieFilepath=`echo ${line} | cut -d ',' -f4`
bwaFilepath=`echo ${line} | cut -d ',' -f5`

mkdir -p `dirname ${dbFilepath}`
sqlite3 ${dbFilepath} --init schema.sql
./import_db.py ${dbFilepath} ${fastqFilepath} ${scaffFilepath} ${bowtieFilepath} ${bwaFilepath}
