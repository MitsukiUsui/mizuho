#!/usr/bin/env python3

import pandas as pd
from Bio import SeqIO
import os
import sys

from taxonomy import get_result_df

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
    with open(samFilepath, "r") as f:
        for line in f:
            if line[0]!='@':
                break
        dct_lst.append(parse_line(line))
        for line in f:
            dct_lst.append(parse_line(line))
    sam_df=pd.DataFrame(dct_lst)
    sam_df=sam_df.dropna()
    return sam_df

def main(samFilepath, resultFilepath):
    sam_df=get_sam_df(samFilepath)
    result_df=get_result_df(resultFilepath)
    join_df=pd.merge(sam_df, result_df, on="key")
    join_df=join_df.sort_values(by=["read_name"])
    
    numReads=sam_df.shape[0]
    numReadsAligned=join_df.shape[0]
    print("FOUND: {0}/{1} ({2:.2f}%) reads are aligned".format(numReadsAligned, numReads, float(numReadsAligned) / numReads * 100), flush=True)
    
    readName2binId={}
    prevReadName=""
    prevBinId=-1
    for readName, binId in zip(join_df["read_name"], join_df["bin_id"]):
        if readName != prevReadName:
            prevReadName=readName
            prevBinId=binId
        elif readName == prevReadName and binId == prevBinId: #update only when the same set comes
            readName2binId[readName]=int(binId)
    numReadsBinned=len(readName2binId) * 2
    print("FOUND: {0}/{1} ({2:.2f}%) reads will be binned".format(numReadsBinned, numReads, float(numReadsBinned) / numReads * 100), flush=True)
    
    numBins=result_df["bin_id"].max()
    for direction in ("R1", "R2"):
        inFilepath="/work/GoryaninU/mitsuki/out/spades/mizuho/{0}/filtered/{0}_{1}.fastq".format(sampleId, direction)
        print("START: devide {} into {} bins".format(inFilepath, numBins), flush=True)
        record_lstlst=[[] for _ in range(numBins)]
        for record in SeqIO.parse(inFilepath, "fastq"):
            if record.id in readName2binId:
                binId=readName2binId[record.id]
                record_lstlst[binId - 1].append(record) ## record_lstlst is 0 origin
        
        for i, record_lst in enumerate(record_lstlst):
            binId = i + 1
            outDirec="/work/GoryaninU/mitsuki/out/binning/bin/bin{:03d}".format(binId)
            os.makedirs(outDirec, exist_ok=True)
            outFilepath="{}/{}_{}.fastq".format(outDirec, sampleId, direction)
            with open(outFilepath, "w") as f:
                for record in record_lst:
                    SeqIO.write(record, f, "fastq")
            print("\tDONE: output {} seqs to {}".format(len(record_lst), outFilepath), flush=True)

if __name__=="__main__":
    sampleId=sys.argv[1] 
    samFilepath="/work/GoryaninU/mitsuki/out/binning/bowtie/{}/all.sam".format(sampleId)
    resultFilepath="/work/GoryaninU/mitsuki/out/binning/metagen/all/output/segs.txt"
    main(samFilepath, resultFilepath)
