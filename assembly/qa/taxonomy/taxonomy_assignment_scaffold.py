#!/usr/bin/env python3

import sys
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

def main(geneFilepath, scaffFilepath):
    gene_df=pd.read_csv(geneFilepath)
    
    dct_lst=[]
    for assemname in sorted(set(gene_df["assembly_name"])):
        print("START: process {}".format(assemname))
        assem_df=gene_df[gene_df["assembly_name"]==assemname]
        for scaffname in sorted(set(assem_df["scaffold_name"])):
            scaff_df=assem_df[assem_df["scaffold_name"]==scaffname]
            
            dct={}
            dct["assembly_name"]=assemname
            dct["scaffold_name"]=scaffname
            total=scaff_df.shape[0]

            thres=0.5
            rank_lst=["superkingdom", "phylum", "class", "order", "family", "genus", "species"]
            inProcess = True
            for rank in rank_lst:
                if inProcess:
                    m=stats.mode(scaff_df[rank])
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
        
    out_df=pd.DataFrame(dct_lst)
    out_df=out_df[["assembly_name", "scaffold_name"] + rank_lst]
    out_df.to_csv(scaffFilepath, index=False)
    print("DONE: output to {}".format(scaffFilepath))

if __name__=="__main__":
    baseDirec=sys.argv[1]
    mmseqsDirec="{}/mmseqs".format(baseDirec)
    geneFilepath="{}/taxonomy_gene.csv".format(mmseqsDirec)
    scaffFilepath="{}/taxonomy_scaffold.csv".format(mmseqsDirec)
    main(geneFilepath, scaffFilepath)
