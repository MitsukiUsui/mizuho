#!/usr/bin/env python3

import os
import pandas as pd
from scipy import stats
from ete3 import NCBITaxa
ncbi = NCBITaxa() 

def translator(taxid):
    """
    given taxid, return scientific name
    """
    try:
        return ncbi.get_taxid_translator([taxid])[taxid]
    except KeyError:
        return None

def main(baseDirec, assemname_lst):
    dct_lst=[]
    for assemname in assemname_lst:
        assemDirec="{}/{}".format(baseDirec, assemname)
        scaffname_lst=sorted([f.name for f in os.scandir(assemDirec) if f.is_dir()])
        for scaffname in scaffname_lst:
            inFilepath="{}/{}/taxonomy.csv".format(assemDirec, scaffname)
            if os.path.exists(inFilepath):
                print("START: process {}".format(inFilepath))
                df=pd.read_csv(inFilepath)

                dct={}
                dct["assembly_name"]=assemname
                dct["scaffold_name"]=scaffname
                total=df.shape[0]

                thres=0.5
                rank_lst=["superkingdom", "phylum", "class", "order", "family", "genus", "species"]
                inProcess=True
                for rank in rank_lst:
                    if inProcess:
                        m=stats.mode(df[rank])
                        taxid=m[0][0]
                        count=m[1][0]
                        if (taxid != 0) and (count > total * thres) :
                            dct[rank]="{0} ({1:.2f}%)".format(translator(taxid), count/total*100)
                        else:
                            dct[rank]=""
                            inProcess=False
                    else:
                        dct[rank]=""
                dct_lst.append(dct)
            else:
                print("WARN: not exists {}".format(inFilepath))
        
    out_df=pd.DataFrame(dct_lst)
    out_df=out_df[["assembly_name", "scaffold_name"] + rank_lst]
    outFilepath="{}/taxonomy.csv".format(baseDirec)
    out_df.to_csv(outFilepath, index=False)
    print("DONE: output to {}".format(outFilepath))

if __name__=="__main__":
    baseDirec="/work/GoryaninU/mitsuki/out/taxonomy"
    listFilepath="assembly.list"
    df=pd.read_csv(listFilepath, header=None)
    assemname_lst=list(df[0])
    main(baseDirec, assemname_lst)