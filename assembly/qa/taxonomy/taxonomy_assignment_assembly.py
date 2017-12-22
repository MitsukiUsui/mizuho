#!/usr/bin/env python3

import sys
import os
import pandas as pd
from scipy import stats
from ete3 import NCBITaxa
ncbi = NCBITaxa()
rank_lst=["superkingdom", "phylum", "class", "order", "family", "genus", "species"]

def translator(taxid):
    """
    given taxid, return scientific name
    """
    try:
        return ncbi.get_taxid_translator([taxid])[taxid]
    except KeyError:
        return None
    
def majority_vote(df):
    """
    assign taxonomy by majority vote from top to down
    results are return by dictionary
    """
    
    dct={}
    total=df.shape[0]
    thres=0.5
    
    inProcess = True
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
    return dct

def main(geneFilepath, assemFilepath):
    gene_df=pd.read_csv(geneFilepath)
    
    dct_lst=[]
    for assemname in sorted(set(gene_df["assembly_name"])):
        print("START: process {}".format(assemname))
        assem_df=gene_df[gene_df["assembly_name"]==assemname]
        dct={"assembly_name": assemname}
        dct.update(majority_vote(assem_df))
        dct_lst.append(dct)
        
    out_df=pd.DataFrame(dct_lst)
    out_df=out_df[["assembly_name"] + rank_lst]
    out_df.to_csv(assemFilepath, index=False)
    print("DONE: output to {}".format(assemFilepath))

if __name__=="__main__":
    baseDirec=sys.argv[1]
    geneFilepath="{}/taxonomy_gene.csv".format(baseDirec)
    assemFilepath="{}/taxonomy_assembly.csv".format(baseDirec)
    main(geneFilepath, assemFilepath)
    
