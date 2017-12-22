#!/bin/bash

get_stat () {
    seqFilepath=${1}
    statFilepath=${seqFilepath/.fastq*/.stat}
    seqkit stat --tabular --threads 4 ${seqFilepath} > ${statFilepath}
}

IFS=$'\n'
array=`tail -n +2 filepath_dna.csv`

seqDirec=/work/GoryaninU/mitsuki/mizuho/dna/row
for line in ${array[@]}
do 
    row=`echo ${line}|cut -d "," -f4`
    sango=`echo ${line}|cut -d "," -f6`
    echo "${sango},${row}"
#    ln -s ${sango} ${filepath}
#    get_stat ${filepath}
done
