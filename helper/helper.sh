#!/bin/bash

module load samtools

sam2bam () {
    samFilepath=${1}
    bamFilepath=${samFilepath/.sam/.bam}
    echo "START: output ${bamFilepath} from ${samFilepath}"
    samtools view -Sb ${samFilepath} | samtools sort -o ${bamFilepath}
    samtools index ${bamFilepath}
    rm ${samFilepath} #sam is too large for storing information
}
