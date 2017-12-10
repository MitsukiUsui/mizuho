#!/bin/bash

IFS=$'\n'
array=`tail -n +2 bin.list`

outDirec=/work/GoryaninU/mitsuki/out/checkm/in
mkdir -p ${outDirec}
for line in ${array[@]}
do 
    binId=`echo ${line}|cut -d "," -f1`
    filepath=`echo ${line}|cut -d "," -f2`
    outFilepath="${outDirec}/${binId}.fna"
    ln -s ${filepath} ${outFilepath}
done
