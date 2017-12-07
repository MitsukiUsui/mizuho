#!/bin/bash

get_stat () {
    seqFilepath=${1}
    statFilepath=${seqFilepath/.fastq*/.stat}
    seqkit stat --tabular --threads 4 ${seqFilepath} > ${statFilepath}
}

IFS=$'\n'
array=`tail -n +2 mizuho_metadata_rna.csv`

seqDirec=/work/GoryaninU/mitsuki/mizuho/rna/row
for line in ${array[@]}
do 
    fastqId=`echo ${line}|cut -d "," -f1`
    filepath="${seqDirec}/${fastqId}.fastq.gz"
    #sango=`echo ${line}|cut -d "," -f3`
    #ln -s ${sango} ${filepath}
    get_stat ${filepath}
done
