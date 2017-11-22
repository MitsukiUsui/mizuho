#!/bin/bash

module load samtools

#merge multiple bam
arr=($@)
str="$(IFS=" ";echo "${arr[*]}")"
cmd="samtools merge --thread 8 "${str}
echo ${cmd}
#eval ${cmd}

#convert to sam
bamFilepath=${1}
samFilepath=${bamFilepath/.bam/.sam}
samtools view -h -o ${samFilepath} ${bamFilepath}
