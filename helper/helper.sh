#!/bin/bash

module load samtools

sam2bam () {
    samFilepath=${1} ##WARNING only works with `sam2bam ${samFilepath} (-d)`
    getopts "d" opts

    bamFilepath=${samFilepath/.sam/.bam}
    echo "START: output ${bamFilepath} from ${samFilepath}"
    samtools view -Sb ${samFilepath} | samtools sort -o ${bamFilepath}
    samtools index ${bamFilepath}

    if [ "$opts" = d ]; then
        rm ${samFilepath}
        echo "DONE: delete ${samFilepath}"
    fi
}
