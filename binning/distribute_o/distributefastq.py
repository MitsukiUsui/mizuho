#!/usr/bin/env python3

import pandas as pd
from Bio import SeqIO
import os
import sys

from distribute import get_result_df

def get_sam_df(samFilepath):
    
    def parse_line(line):
        """
        return: success, binId, readName
        """
        dct={}
        try:
            #WARNING: it seems .sam contains incomplete lines. 
            #those line will be ignored in the distribution process, so do not care for now.
            lineSplited=line.strip().split("\t")
            dct["read_name"]=lineSplited[0]
            dct["key"]=lineSplited[2]
        except:
            print("WARN: unusual line \"{}\" found".format(line.strip()))
            return dict()
        return dct
    
    dct_lst=[]
    with open(samFilepath, "r", errors="ignore") as f:
        for line in f:
            if line[0]!='@':
                break
        dct_lst.append(parse_line(line))
        for line in f:
            dct_lst.append(parse_line(line))
    sam_df=pd.DataFrame(dct_lst)
    sam_df=sam_df.dropna()
    return sam_df

def main(sampleId, binningDirec):
    samFilepath="{}/distribute/bowtie/map/{}.sam".format(binningDirec, sampleId)
    resultFilepath="{}/metagen/output/segs.txt".format(binningDirec)
    
    print("START: load {}".format(samFilepath))
    sam_df=get_sam_df(samFilepath)
    print("START: load {}".format(resultFilepath))
    result_df=get_result_df(resultFilepath)
    print("START: join ")
    join_df=pd.merge(sam_df, result_df, on="key")
    join_df=join_df.sort_values(by=["read_name"])
    
    readName2binId={}
    prevReadName=""
    for readName, binId in zip(join_df["read_name"], join_df["bin_id"]):
        if readName != prevReadName:
            readName2binId[readName]=set([int(binId)])
            prevReadName=readName
        else:
            readName2binId[readName].add(int(binId))
    print("DONE: create readName2binId")
            
    numBins=result_df["bin_id"].max()
    for direction in ("R1", "R2"):
        inFilepath="/work/GoryaninU/mitsuki/out/spades/mizuho/{0}/filtered/{0}_{1}.fastq".format(sampleId, direction)
        print("START: devide {} into {} bins".format(inFilepath, numBins), flush=True)
        record_lstlst=[[] for _ in range(numBins)]
        
        recordCount=0
        assignedCount=0
        binCount=0
        for record in SeqIO.parse(inFilepath, "fastq"):
            recordCount+=1
            if record.id in readName2binId:
                assignedCount+=1
                for binId in readName2binId[record.id]:
                    binCount+=1
                    record_lstlst[binId - 1].append(record) ## record_lstlst is 0 origin
        
        print("START: distribute {}/{} ({:.2f}%) seqs into bins".format(assignedCount, recordCount, float(assignedCount)/recordCount * 100))
        print("\tduplication found {} times".format(binCount-assignedCount))
        for i, record_lst in enumerate(record_lstlst):
            binId = i + 1
            outDirec="{}/distribute/bin{:03d}".format(binningDirec, binId)
            os.makedirs(outDirec, exist_ok=True)
            outFilepath="{}/{}_{}.fastq".format(outDirec, sampleId, direction)
            with open(outFilepath, "w") as f:
                for record in record_lst:
                    SeqIO.write(record, f, "fastq")
            print("\tDONE: output {} seqs to {}".format(len(record_lst), outFilepath), flush=True)

if __name__=="__main__":
    sampleId=sys.argv[1]
    binningDirec="/work/GoryaninU/mitsuki/out/binning"
    main(sampleId, binningDirec)
