#!/usr/bin/env python3

import pandas as pd
import sys
import os
from Bio import SeqIO

sys.path.append("/home/m/mitsuki-usui/mizuho/assembly/qa/map")
from MapDbController import MapDbController

def get_readId2binId(mdc):
    """
    key: readId, val: set of binId distributed to
    """
    
    print("START: match readId to binIds")
    query=("SELECT bowtie.read_id, ref.bin_id "\
          +"FROM bowtie "\
          +"INNER JOIN ref on bowtie.scaff_id = ref.scaff_id")
    success=mdc.execute(query)
    if success:
        results=mdc.cur.fetchall()
        readId2binId={}
        for result in results:
            readId=result["read_id"]
            binId=result["bin_id"]
            if readId in readId2binId.keys():
                readId2binId[readId].update([binId])
            else:
                readId2binId[readId]=set([binId])
        return readId2binId
    else:
        print("ERROR: query failed")
        print("\t{}".format(query))
        return None
                

def main(sampleId, numBins, dbFilepath, seqDirec, baseDirec):
    mdc=MapDbController(dbFilepath)
    readId2binId=get_readId2binId(mdc)
    
    for direction in ("R1", "R2"):
        inFilepath="{}/{}_{}.fastq".format(seqDirec, sampleId, direction)
        print("START: devide {} into {} bins".format(inFilepath, numBins), flush=True)

        rc=0 #record count
        arc=0 # assigned record count
        ac=0 # assign count
        record_lstlst=[[] for _ in range(numBins)]
        for readId, record in enumerate(SeqIO.parse(inFilepath, "fastq")): # WARN: depends on definition of readId
            rc += 1
            if readId in readId2binId.keys():
                arc += 1
                for binId in readId2binId[readId]:
                    ac += 1
                    record_lstlst[binId - 1].append(record)
        print("START: distribute {}/{} ({:.2f}%) records into bins".format(arc, rc, float(arc) /rc * 100))
        print("\tduplication found {}/{} ({:.2f}%) times".format(ac-arc, arc, float(ac-arc) / arc * 100))

        for _, record_lst in enumerate(record_lstlst):
            binId = _ + 1
            outDirec="{}/ref{:03d}".format(baseDirec, binId)
            os.makedirs(outDirec, exist_ok=True)
            outFilepath="{}/{}_{}.fastq".format(outDirec, sampleId, direction)
            with open(outFilepath, "w") as f:
                for record in record_lst:
                    SeqIO.write(record, f, "fastq")
            print("\tDONE: output {} seqs to {}".format(len(record_lst), outFilepath), flush=True)

if __name__=="__main__":
    sampleId=sys.argv[1]  # "MFC1_36m_anode1"
    numBins=67
    dbFilepath="/work/GoryaninU/mitsuki/out/map/db/ref/{}.sq3".format(sampleId)
    seqDirec="/work/GoryaninU/mitsuki/mizuho/dna/filter"
    baseDirec="/work/GoryaninU/mitsuki/out/distribute/ref" #splitted files will be placed under ./ref001/${sampleId}_R1.fastq
    main(sampleId, numBins, dbFilepath, seqDirec, baseDirec)
