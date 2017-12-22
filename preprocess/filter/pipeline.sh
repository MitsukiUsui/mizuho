#!/bin/bash

#SBATCH --job-name=preprocess
#SBATCH --partition=largemem
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --input=none
#SBATCH --output=./log/preprocess_%A_%a.out
#SBATCH --error=./log/preprocess_%A_%a.err
#SBATCH --mem=200g
#SBATCH --time=1-00 


get_stat () {
    seqFilepath=${1}
    statFilepath=${seqFilepath/.fastq*/.stat}
    seqkit stat --tabular --threads 4 ${seqFilepath} > ${statFilepath}
}

#--------------------------------------------------------------------------------
# array job expander
#--------------------------------------------------------------------------------
argFilepath=${1}
if [ -z ${SLURM_ARRAY_TASK_ID+x} ]; then lineNum=1; else lineNum=${SLURM_ARRAY_TASK_ID}; fi;
line=`awk -v lineNum=$lineNum '{if (NR == lineNum) print $0}' ${argFilepath}`
baseDirec=`echo ${line} | cut -d ',' -f1`
sampleId=`echo ${line} | cut -d ',' -f2`

leftFastqId=${sampleId}_R1
rightFastqId=${sampleId}_R2
# input raw fastq.gz
rawLeftFilepath=${baseDirec}/raw/${leftFastqId}.fastq.gz
rawRightFilepath=${baseDirec}/raw/${rightFastqId}.fastq.gz
# trimed fastq
trimLeftFilepath=${baseDirec}/trim/${leftFastqId}.fastq
trimRightFilepath=${baseDirec}/trim/${rightFastqId}.fastq
#corrected fastq
spadesDirec=${baseDirec}/correct/${sampleId}
corLeftFilepath=${spadesDirec}/corrected/${leftFastqId}.00.0_0.cor.fastq.gz
corRightFilepath=${spadesDirec}/corrected/${rightFastqId}.00.0_0.cor.fastq.gz
#filtered fastq
filterLeftFilepath=${baseDirec}/filter/${leftFastqId}.fastq
filterRightFilepath=${baseDirec}/filter/${rightFastqId}.fastq

echo "START: process ${rawLeftFilepath}, ${rawRightFilepath}"

#--------------------------------------------------------------------------------
# check existance of target file
#--------------------------------------------------------------------------------
FORCE_MODE=true
forceFilepath=${filterRightFilepath}
if [ "$FORCE_MODE" = false ] && [ -e ${forceFilepath} ]; then
    echo "PASS: target file already exists"
    exit
fi

#--------------------------------------------------------------------------------
# get stats (raw)
#--------------------------------------------------------------------------------
get_stat ${rawLeftFilepath}
get_stat ${rawRightFilepath}

#--------------------------------------------------------------------------------
# trim adapter & dirty ends
#--------------------------------------------------------------------------------
echo "START: trim ${rawLeftFilepath}, ${rawRightFilepath}"

tmpLeftFilepath=${trimLeftFilepath/.fastq/.tmp.fastq}
tmpRightFilepath=${trimRightFilepath/.fastq/.tmp.fastq}

module load python/3.5.0
time cutadapt -a AGATCGGAAGAGCACACGTCTGAACTCCAGTCA \
              -A AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT \
              -o ${tmpLeftFilepath} \
              -p ${tmpRightFilepath} \
              --minimum-length 100 \
              ${rawLeftFilepath} ${rawRightFilepath}
time cutadapt --cut 10 --cut -5 \
              -o ${trimLeftFilepath} ${tmpLeftFilepath}
time cutadapt --cut 10 --cut -5 \
              -o ${trimRightFilepath} ${tmpRightFilepath}
module load python/3.5.0

rm ${tmpLeftFilepath}
rm ${tmpRightFilepath}
get_stat ${trimLeftFilepath}
get_stat ${trimRightFilepath}

#--------------------------------------------------------------------------------
# read correction by BayesHammer in metaSPAdes
#--------------------------------------------------------------------------------
echo "START: correct ${trimLeftFilepath}, ${trimRightFilepath}"
time ~/software/SPAdes-3.11.1-Linux/bin/spades.py --meta --only-error-correction \
                                                  -1 ${trimLeftFilepath} \
                                                  -2 ${trimRightFilepath} \
                                                  -o ${spadesDirec} \
                                                  --threads 8 --memory 200

#--------------------------------------------------------------------------------
# filter reads wich both ends passed BayesHammer
#--------------------------------------------------------------------------------
tmpLeftFilepath=${filterLeftFilepath/.fastq/.tmp.fastq}
tmpRightFilepath=${filterRightFilepath/.fastq/.tmp.fastq}
nameFilepath=`dirname ${filterLeftFilepath}`/${sampleId}.names
echo "START: filter ${corLeftFilepath}, ${corRightFilepath}"

time seqkit grep -nrvp failed ${corLeftFilepath} > ${tmpLeftFilepath}
time seqkit grep -nrvp failed ${corRightFilepath} > ${tmpRightFilepath}
time grep -Fx -f <(fatt name ${tmpLeftFilepath}) <(fatt name ${tmpRightFilepath}) > ${nameFilepath}
time fatt extract --file ${nameFilepath} ${tmpLeftFilepath} > ${filterLeftFilepath}
time fatt extract --file ${nameFilepath} ${tmpRightFilepath} > ${filterRightFilepath}

get_stat ${tmpLeftFilepath}
get_stat ${tmpRightFilepath}
get_stat ${filterLeftFilepath}
get_stat ${filterRightFilepath}

echo "DONE: output ${filterLeftFilepath},${filterRightFilepath}"
