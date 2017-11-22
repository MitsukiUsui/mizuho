#!/bin/bash

module load samtools
inFilepath=${1}
outFilepath=${2}
samtools view -H -o ${outFilepath} ${inFilepath}

