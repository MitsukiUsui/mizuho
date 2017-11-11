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

def main(assemname):
    directory="./tmp/{}".format(assemname)
    outFilepath="./tmp/{}/taxonomy.csv".format(assemname)
    
    scafname_lst=sorted([f.name for f in os.scandir(directory) if f.is_dir()])
    thres=0.5
    rank_lst=["superkingdom", "phylum", "class", "order", "family", "genus", "species"]
    dct_lst=[]
    for scafname in scafname_lst:
        inFilepath="{}/{}/taxonomy.csv".format(directory, scafname)
        if os.path.exists(inFilepath):
            df=pd.read_csv(inFilepath)

            dct={}
            dct["assembly_name"]=assemname
            dct["scaffold_name"]=scafname
            total=df.shape[0]

            for rank in rank_lst:
                m=stats.mode(df[rank])
                taxid=m[0][0]
                count=m[1][0]
                if (taxid != 0) and (count > total * thres) :
                    dct[rank]="{0}({1:.2f}%)".format(translator(taxid), count/total*100)
                else:
                    break
            dct_lst.append(dct)
    
    out_df=pd.DataFrame(dct_lst)
    out_df=out_df[["assembly_name", "scaffold_name"] + rank_lst]
    out_df.to_csv(outFilepath, index=False)

if __name__=="__main__":
    assemname="spades_all"
    main(assemname)