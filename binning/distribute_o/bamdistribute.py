#!/usr/bin/env python3

import pandas as pd
import sys

from distribute import get_result_df

def get_scaffName(line):
    """
    given sam line, return scaffold name
    """

    try:
        #WARNING: it seems .sam contains incomplete lines. 
        #those line will be ignored in the distribution process, so do not care for now.
        return line.strip().split("\t")[2]
    except:
        print("WARN: unusual line \"{}\" found".format(line.strip()))
        return None

def main(assemname, binningDirec):
    resultFilepath="{}/metagen/output/segs.txt".format(binningDirec)
    result_df=get_result_df(resultFilepath)
    scaffName2binId={}
    for scaffName, binId in zip(result_df["key"], result_df["bin_id"]):
        scaffName2binId[scaffName]=binId
    
    samFilepath="{}/metagen/bowtie/map/{}.sam".format(binningDirec, assemName)
    numBins=result_df["bin_id"].max()
    line_lstlst=[[] for _ in range(numBins)]
    print("START: load {}".format(samFilepath), flush=True)
    with open(samFilepath, "r") as fi:
        for line in fi:
            if line[0]!='@':
                break
        
        scaffName=get_scaffName(line)
        if scaffName in scaffName2binId:
            binId=scaffName2binId[get_scaffName(line)]
            line_lstlst[binId - 1].append(line)
        for line in fi:
            scaffName=get_scaffName(line)
            if scaffName in scaffName2binId:
                binId=scaffName2binId[get_scaffName(line)]
                line_lstlst[binId - 1].append(line)
    
    print("START: divide to {} bins".format(numBins))
    for i, line_lst in enumerate(line_lstlst):
        binId = i + 1
        outFilepath="{}/distribute/bin{:03d}/{}.sam".format(binningDirec, binId, assemName)
        with open(outFilepath, "a") as fo:
            for line in line_lst:
                fo.write(line)
        print("\tDONE: {} lines {}".format(len(line_lst), outFilepath), flush=True)

if __name__=="__main__":
    assemName=sys.argv[1]
    binningDirec="/work/GoryaninU/mitsuki/out/binning"
    main(assemName, binningDirec)
