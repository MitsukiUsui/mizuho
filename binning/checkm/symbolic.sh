#!/bin/bash

IFS=$'\n'
array=`tail -n +2 bin.list`

binDirec=/work/GoryaninU/mitsuki/out/bin/36m_anode
outDirec=/work/GoryaninU/mitsuki/out/checkm/36m_anode/metagen/in
mkdir -p ${outDirec}

for binId in `seq -f %03g 84`
do
    inFilepath=${binDirec}/bin${binId}/scaffolds.fasta
    outFilepath=${outDirec}/bin${binId}.fasta
    ln -s ${inFilepath} ${outFilepath}
done
