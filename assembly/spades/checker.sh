while read line
do
    sampleId=`echo ${line}|cut -d "," -f1`
    outDirec=/work/GoryaninU/mitsuki/out/spades/mizuho/${sampleId}
    seqFilepath=${outDirec}/scaffolds.fasta
    if [ -e ${seqFilepath} ]; then
        echo ${sampleId}" pass"
    else
        echo "ERROR: "${sampleId}", scaffolds.fasta does not exist."
    fi

done < ../../preprocess/pair.list
